import requests
from dateutil import parser
import xml.etree.ElementTree as ET
from datetime import datetime

def fetch_rss_feed(url, headers):
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raises HTTPError if the HTTP request returned an unsuccessful status code
    return ET.fromstring(response.content)


def parse_rss_feed(root, source_name):
    articles = []
    for item in root.findall('.//item'):
        article = {child.tag: child.text for child in item}
        article['source'] = source_name
        article['pubDate'] = parser.parse(article['pubDate'])
        print(f"Title ({article['pubDate']}): {article['title']} - {article.get('description', '')} - {article.get('full-text', '')}, Link: {article['link']}")
        articles.append(article)
    return sorted(articles, key=lambda x: x['pubDate'], reverse=False)


def filter_articles(articles, keywords, last_time):
    last_time_dt = datetime.strptime(last_time, "%Y-%m-%d %H:%M:%S")
    print("last_time_dt", last_time_dt)
    w_articles = [article for article in articles if any(
        kw in ((article.get('title') or '') + (article.get('description') or '') + (
                article.get('full-text') or '')).lower()
        for kw in keywords
    ) and article.get("pubDate", datetime.min).replace(tzinfo=None) > last_time_dt]
    w_articles = w_articles[-2:]  # last 2 articles

    if not w_articles:
        print("No new article.")

    return w_articles