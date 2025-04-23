
import feedparser
from bs4 import BeautifulSoup
from newspaper import Article
import logging

logging.basicConfig(level=logging.INFO)

RSS_FEEDS = [
    "https://medium.com/feed/tag/{keyword}",
    "https://dev.to/feed/tag/{keyword}",
    "https://hashnode.com/feed",
    "https://substack.com/feed",
    "https://hnrss.org/newest?q={keyword}",
    "https://www.reddit.com/r/{keyword}/.rss",
    "https://feeds.feedburner.com/{keyword}"
]

def clean_html(html):
    return BeautifulSoup(html, "html.parser").get_text()

def fetch_full_article(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        logging.warning(f"Failed to extract article from {url}: {e}")
        return ""

def fetch_blogs(keyword: str):
    blogs = []

    for feed_template in RSS_FEEDS:
        url = feed_template.format(keyword=keyword.lower().replace(" ", "-"))
        logging.info(f"🔍 Fetching: {url}")

        feed = feedparser.parse(url)
        for entry in feed.entries[:20]:
            link = entry.get("link", "")
            title = entry.get("title", "")
            summary = entry.get("summary", "")
            content = clean_html(summary)

            # Use newspaper3k for better article content if possible
            full_article = fetch_full_article(link)
            final_content = full_article if len(full_article) > 300 else content

            if len(final_content) > 200:
                blogs.append({
                    "title": title,
                    "url": link,
                    "content": final_content
                })

    return blogs
