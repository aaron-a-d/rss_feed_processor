import requests
from openai import OpenAI
from config import settings

def create_telegram_message(article):
    client = OpenAI(api_key=settings.OPENAI_KEY)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"""I want you to act as a translator. You will be given an article and your only task is to build a french Teleram message based on this article. The telegram message will be in french and French only.
The French Telegram message will remain short. Cut some part of the text if it is too long for a french Telegram message. Stick to what you see in the article, NOTHING MORE. The french Telegram message must be attractive and pleasant to read for the reader.
The message must contain a link to the article, the title for the article if any and a description of the article based on the given article.

Article as dictionary: 
```
{article}
```

Short french Telegram message: """,
            }
        ],
        model="gpt-3.5-turbo",
        temperature=0
    )
    article['telegram'] = chat_completion.choices[0].message.content
    return article

def send_to_telegram(articles, chat_id):
    apiURL = f'https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage'

    for article in articles:
        telegram_message = article.get("telegram", "")
        if len(telegram_message) > 10:
            try:
                response = requests.post(apiURL,
                                         json={'chat_id': chat_id, 'text': telegram_message, 'parse_mode': 'Markdown'})
            except Exception as e:
                print(e)

# Add other Telegram related functions here
