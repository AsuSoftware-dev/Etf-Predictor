import yfinance as yf
import requests
from .models import ETFData
from textblob import TextBlob
from .models import NewsSentiment

def fetch_and_save_data(symbol):
    # Fetch data from Yahoo Finance
    data = yf.download(symbol, period="5d", interval="1h")
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
    df['sma_20'] = df['close_price'].rolling(window=20).mean()
    df['sma_50'] = df['close_price'].rolling(window=50).mean()

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
    # Preluăm datele despre ETF din baza de date
    etf_data = ETFData.objects.filter(symbol=symbol).order_by('-date')
    recent_sentiments = NewsSentiment.objects.filter(etf_symbol=symbol).order_by('-published_at')[:10]

    # Calculăm sentimentele pozitive și negative
    positive_news = sum(1 for s in recent_sentiments if s.sentiment == "Positive")
    negative_news = sum(1 for s in recent_sentiments if s.sentiment == "Negative")

    # Verificăm datele despre prețuri și SMA
    last_close = etf_data.first().close_price if etf_data.exists() else None
    sma_20 = etf_data.first().sma_20 if etf_data.exists() else None
    sma_50 = etf_data.first().sma_50 if etf_data.exists() else None

    # Tratăm cazul în care una dintre valori este None
    if last_close is None or sma_20 is None or sma_50 is None:
        return "Insufficient data to make a recommendation"

    # Generăm recomandarea
    if positive_news > negative_news and last_close > sma_20 > sma_50:
        return "Buy"
    elif negative_news > positive_news and last_close < sma_20 < sma_50:
        return "Sell"
    return "Hold"
