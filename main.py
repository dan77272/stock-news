import requests
from datetime import datetime, timedelta
from twilio.rest import Client
import os

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

account_sid = os.environ["ACCOUNT_SID"]
auth_token = os.environ["AUTH_TOKEN"]

today = datetime.today()
yesterday = today - timedelta(days=1)
day_before_yesterday = today - timedelta(days=2)


response = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TSLA&apikey=WILI0TR8CX5R3FYR")
news_response = requests.get("https://newsapi.org/v2/everything?q=tesla&from=2022-04-20&sortBy=publishedAt&apiKey=3dd8be9a416c405ea2ef45bea291ba0c")
response.raise_for_status()
news_response.raise_for_status()
data = response.json()
news_data = news_response.json()

yesterday_closing = data['Time Series (Daily)'][str(yesterday).split(' ', 1)[0]]['4. close']

day_before_yesterday_closing = data['Time Series (Daily)'][str(day_before_yesterday).split(' ', 1)[0]]['4. close']

stock_difference = abs(float(yesterday_closing) - float(day_before_yesterday_closing))
stock_sum = float(yesterday_closing) + float(day_before_yesterday_closing)
difference_percentage = (stock_difference / (stock_sum + 2)) * 100
latest_articles = [article for article in news_data['articles'][:3]]


if difference_percentage > 0.01:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body=f"Tesla Stock News: {latest_articles[0]['description']} {latest_articles[0]['url']}",
        from_=PHONE_NUMBER,
        to=PHONE_NUMBER2
    )
    print(message.status)
