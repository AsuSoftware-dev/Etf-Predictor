import yfinance as yf
import requests
from .models import ETFData
from textblob import TextBlob
from .models import NewsSentiment

def fetch_and_save_data(symbol):
    # Fetch data from Yahoo Finance
    data = yf.download(symbol, period="6mo", interval="1d")
    print(data.head())
    for date, row in data.iterrows():
        ETFData.objects.update_or_create(
            symbol=symbol,
            date=date,
            defaults={
                'open_price': row['Open'],
                'close_price': row['Close'],
                'high': row['High'],
                'low': row['Low'],
                'volume': row['Volume'],
            }
        )


def calculate_sma(symbol):
    from pandas import DataFrame
    data = ETFData.objects.filter(symbol=symbol).order_by('date')
    df = DataFrame(list(data.values()))

    # Debugging: Verifică datele înainte de calcul
    print("Data before SMA calculation:")
    print(df)

    # Calculăm SMA
    df['sma_20'] = df['close_price'].rolling(window=20).mean()
    df['sma_50'] = df['close_price'].rolling(window=50).mean()

    # Debugging: Verifică SMA calculat
    print("Data with SMA:")
    print(df[['close_price', 'sma_20', 'sma_50']])

    for _, row in df.iterrows():
        obj = ETFData.objects.get(pk=row['id'])
        obj.sma_20 = row['sma_20']
        obj.sma_50 = row['sma_50']
        obj.save()


def fetch_and_analyze_news(etf_symbol):
    # Fetch news data from NewsAPI
    api_key = "b0e3c702a1644de381c468939532958a"
    url = f"https://newsapi.org/v2/everything?q={etf_symbol}&apiKey={api_key}"
    response = requests.get(url)
    articles = response.json().get("articles", [])

    for article in articles:
        title = article["title"]
        sentiment = analyze_sentiment(title)
        published_at = article["publishedAt"]

        # Save sentiment data to the database
        NewsSentiment.objects.update_or_create(
            etf_symbol=etf_symbol,
            title=title,
            defaults={
                'sentiment': sentiment,
                'published_at': published_at,
            }
        )

def analyze_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    return "Neutral"

def generate_recommendation(symbol):
    etf_data = ETFData.objects.filter(symbol=symbol).order_by('-date')
    if len(etf_data) < 50:
        return "Insufficient historical data to make a recommendation"

    # Extrage ultimul rând cu valori SMA valide
    last_valid_entry = etf_data.exclude(sma_20__isnull=True, sma_50__isnull=True).first()

    if not last_valid_entry:
        return "No valid SMA data available"

    last_close = last_valid_entry.close_price
    sma_20 = last_valid_entry.sma_20
    sma_50 = last_valid_entry.sma_50

    print(f"Last Close: {last_close}, SMA 20: {sma_20}, SMA 50: {sma_50}")

    # Adaugă logică de recomandare
    positive_news = sum(1 for s in NewsSentiment.objects.filter(etf_symbol=symbol, sentiment="Positive"))
    negative_news = sum(1 for s in NewsSentiment.objects.filter(etf_symbol=symbol, sentiment="Negative"))

    if positive_news > negative_news and last_close > sma_20 > sma_50:
        return "Buy"
    elif negative_news > positive_news and last_close < sma_20 < sma_50:
        return "Sell"
    return "Hold"
