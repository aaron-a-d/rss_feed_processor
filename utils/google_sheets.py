from google.oauth2.service_account import Credentials
import gspread
from config import settings
from datetime import datetime, timedelta


def get_last_article_from_sheets(sheet, source_name):
    last_article = max((rec for rec in sheet.get_all_records() if rec['source'] == source_name),
                       key=lambda x: x['pubDate'],
                       default=None)
    if last_article:
        return last_article.get("pubDate", "")
    else:
        return (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")


def authenticate_google_sheets(spreadsheet_id):
    scope = ["https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file(settings.CREDENTIALS_FILE, scopes=scope)
    client = gspread.authorize(creds)
    return client.open_by_key(spreadsheet_id)


def append_to_sheet(sheet, articles, column_headers):
    for article in articles:
        # Convert datetime to string before appending
        row_values = [article.get(header, '') if not isinstance(article.get(header), datetime)
                      else article.get(header).strftime("%Y-%m-%d %H:%M:%S")
                      for header in column_headers]
        sheet.append_row(row_values)
        print("Added")
