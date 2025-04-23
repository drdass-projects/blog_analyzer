from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from empath import Empath

vader = SentimentIntensityAnalyzer()
empath = Empath()

def analyze_blogs(blogs):
    for blog in blogs:
        text = blog["content"][:1000]

        vader_result = vader.polarity_scores(text)
        blog["vader_compound"] = vader_result["compound"]
        blog["vader_sentiment"] = (
            "Positive" if vader_result["compound"] >= 0.05 else
            "Negative" if vader_result["compound"] <= -0.05 else
            "Neutral"
        )

        empath_result = empath.analyze(text, normalize=True)
        tags = sorted(empath_result.items(), key=lambda x: x[1], reverse=True)[:3]
        blog["empath_tags"] = ", ".join([cat for cat, score in tags if score > 0.05]) or "None"

    return blogs
