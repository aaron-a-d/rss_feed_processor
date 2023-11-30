import requests
from config import settings
import xml.etree.ElementTree as ET
from utils import google_sheets, rss_feed, telegram


# def main():
format_string = "%a, %d %b %Y %H:%M:%S %z"
headers = {'User-Agent': 'Mozilla/5.0'}
sheets = google_sheets.authenticate_google_sheets(settings.SPREADSHEET_ID)
sheet_articles = sheets.worksheet("articles")
sheet_rss = sheets.worksheet("RSS")
sheet_keywords = sheets.worksheet("keywords")
keywords = [k.lower() for k in sheet_keywords.col_values(1)]
sources = sheet_rss.get_all_records()

for source in sources:
    try:
        rss_link = source['link']
        source_name = source['name']

        latest_article = google_sheets.get_last_article_from_sheets(sheet_articles, source_name)

        root = rss_feed.fetch_rss_feed(rss_link, headers)
        articles = rss_feed.parse_rss_feed(root, source_name)

        articles_filtered = rss_feed.filter_articles(articles, keywords, latest_article)
        print(f"{len(articles_filtered)} articles to publish.")
        articles_filtered_telegram = [telegram.create_telegram_message(article) for article in articles_filtered]
        column_headers = sheet_articles.row_values(1)
        google_sheets.append_to_sheet(sheet_articles, articles_filtered, column_headers)
        telegram.send_to_telegram(articles_filtered_telegram, settings.CHANNEL_NAME)
    except requests.HTTPError as e:
        print(f"HTTP Error: {e}")
    except ET.ParseError as e:
        print(f"XML Parsing Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# return articles
#
#
# if __name__ == "__main__":
#     articles = main()
