import requests
from twilio.rest import Client

# -------------------- CONFIG -------------------- #

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "YOUR_ALPHA_VANTAGE_API_KEY"
NEWS_API_KEY = "YOUR_NEWSAPI_KEY"

TWILIO_SID = "YOUR_TWILIO_SID"
TWILIO_AUTH_TOKEN = "YOUR_TWILIO_AUTH_TOKEN"

VIRTUAL_TWILIO_NUMBER = "YOUR_TWILIO_PHONE_NUMBER"
VERIFIED_NUMBER = "YOUR_VERIFIED_PHONE_NUMBER"

# -------------------- STOCK DATA -------------------- #

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
response.raise_for_status()

data = response.json()["Time Series (Daily)"]
data_list = [value for value in data.values()]

yesterday_close = float(data_list[0]["4. close"])
day_before_close = float(data_list[1]["4. close"])

difference = yesterday_close - day_before_close

if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

diff_percent = round(abs(difference) / day_before_close * 100)

# -------------------- NEWS DATA -------------------- #

if diff_percent > 5:

    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
        "language": "en",
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    news_response.raise_for_status()

    articles = news_response.json()["articles"]
    three_articles = articles[:3]

    formatted_articles = [
        f"{STOCK_NAME}: {up_down}{diff_percent}%\n"
        f"Headline: {article['title']}\n"
        f"Brief: {article['description']}"
        for article in three_articles
    ]

    # -------------------- SEND SMS -------------------- #

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=VIRTUAL_TWILIO_NUMBER,
            to=VERIFIED_NUMBER
        )

        print(message.sid)

else:
    print("Stock change less than 5%. No news sent.")