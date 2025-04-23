import feedparser
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)

RSS_FEEDS = [
    "https://medium.com/feed/tag/{keyword}",
    "https://dev.to/feed/tag/{keyword}",
    "https://hashnode.com/feed",
    "https://substack.com/feed",
    "https://news.ycombinator.com/rss",
    "https://hnrss.org/newest?q={keyword}",
    "https://feeds.feedburner.com/{keyword}",
    "https://www.reddit.com/r/{keyword}/.rss"
]

def clean_html(html):
    return BeautifulSoup(html, "html.parser").get_text()

def fetch_blogs(keyword: str):
    blogs = []

    for feed_template in RSS_FEEDS:
        url = feed_template.format(keyword=keyword.lower().replace(" ", "-"))
        logging.info(f"🔍 Fetching: {url}")

        feed = feedparser.parse(url)
        for entry in feed.entries[:20]:  # Increase from 5 to 20
            content = clean_html(entry.get("summary", "") or entry.get("content", [{"value": ""}])[0]["value"])
            if len(content) > 100:
                blogs.append({
                    "title": entry.get("title", ""),
                    "url": entry.get("link", ""),
                    "content": content
                })

    return blogs
