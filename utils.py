import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()
HASHTAG_RE = re.compile(r"#(\w+)", re.UNICODE)

def compute_sentiment(text: str) -> float:
    if not text:
        return 0.0
    return analyzer.polarity_scores(text)["compound"]

def extract_hashtags(text: str):
    if not text:
        return []
    return [h.lower() for h in HASHTAG_RE.findall(text)]

def compute_engagement_row(likes: int, comments: int, shares: int, followers: int) -> float:
    denom = max(1, int(followers or 0))
    return (int(likes or 0) + int(comments or 0) + int(shares or 0)) / denom
