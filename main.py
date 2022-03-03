from datetime import date
import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_API_KEY = "DQQDH3NV7NXY1RQG"
NEWS_API_KEY = "02234b397b4c452a9e5f09e686bd8fbe"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
TWILIO_SID = "ACb9bd00773b02b240af801a3d935f2e86"
TWILIO_AUTH_TOKEN = "028093cdc1a70e153e82527121d18f41"

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY,
}
news_parameters = {
    "q": f"+{COMPANY_NAME}",
    "apiKey": NEWS_API_KEY,
    "searchIn": "title",
    "language": "en",
    "sortBy": "popularity",
    "pageSize": 1
}


def percentage_change():
    percentage_difference = ((yesterday_close - day_before_close) / yesterday_close) * 100
    return round(percentage_difference, 2)


def increase_or_decrease():
    if percent_change > 0:
        return True
    elif percent_change == 0:
        pass
    else:
        return False


response = requests.get(url=STOCK_ENDPOINT, params=stock_parameters)
stock_data = response.json()["Time Series (Daily)"]
stock_data_list = [value for (key, value) in stock_data.items()]

yesterday_close = float(stock_data_list[0]["4. close"])
day_before_close = float(stock_data_list[1]["4. close"])
abs_difference = abs(yesterday_close - day_before_close)

percent_change = percentage_change()
if percent_change <= -5.00 or percent_change >= 5.00:
    print(f"{STOCK} went up {percent_change}%.\n Price: ${yesterday_close}")
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_parameters)
    news = news_response.json()["articles"]
    try:
        top_three_articles = news[:3]
    except IndexError:
        top_three_articles = news

    formatted_articles = [f"Headline:{article['title']}\nBrief: {article['description']}" for article in top_three_articles]

    if increase_or_decrease():
        for article in formatted_articles:
            print(f"{STOCK}: 🔺{percent_change}%\n{article}")
            client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
            message = client.messages.create(
                body=f"{STOCK}: 🔺{percent_change}%\n{article}",
                from_='+19105698924',
                to='+2347063529084',
            )
    else:
        for article in formatted_articles:
            print(f"{STOCK}: 🔻{percent_change}%\n{article}")
            client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
            message = client.messages.create(
                body=f"{STOCK}: 🔻{percent_change}%\n{article}",
                from_='+19105698924',
                to='+2347063529084',
            )

    print(message.status)
else:
    if increase_or_decrease():
        print(f"{STOCK} went up {percent_change}%.\n Price: ${yesterday_close}")
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        message = client.messages \
            .create(
                body=f"{STOCK} went up {percent_change}%.\n Price: ${yesterday_close}",
                from_='+19105698924',
                to='+2347063529084',
            )
    else:
        print(f"{STOCK} went down {percent_change}%.\n Price: ${yesterday_close}")
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        message = client.messages \
            .create(
                body=f"{STOCK} went down {percent_change}%.\n Price: ${yesterday_close}",
                from_='+19105698924',
                to='+2347063529084',
            )
    print(message.status)
