from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import NewsSentiment, ETFData
from .utils import fetch_and_save_data, calculate_sma, fetch_and_analyze_news, generate_recommendation

@api_view(['GET'])
def analyze_etf(request, symbol):
    try:
        # 1. Preluăm datele ETF și calculăm SMA
        fetch_and_save_data(symbol)
        calculate_sma(symbol)

        # 2. Preluăm știrile și analizăm sentimentul
        fetch_and_analyze_news(symbol)

        # 3. Generăm recomandarea pe baza datelor financiare și a știrilor
        recommendation = generate_recommendation(symbol)

        return Response({"symbol": symbol, "recommendation": recommendation})
    except ValueError as e:
        return Response({"error": str(e)}, status=400)
    except Exception as e:
        return Response({"error": "An unexpected error occurred."}, status=500)

@api_view(['GET'])
def get_financial_data(request, symbol):
    try:
        data = ETFData.objects.filter(symbol=symbol).order_by('date')
        response = [
            {
                "date": entry.date,
                "open_price": entry.open_price,
                "close_price": entry.close_price,
                "high": entry.high,
                "low": entry.low,
                "volume": entry.volume,
                "sma_20": entry.sma_20,
                "sma_50": entry.sma_50,
            }
            for entry in data
        ]
        return Response(response)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['GET'])
def get_news_data(request, symbol):
    try:
        news = NewsSentiment.objects.filter(etf_symbol=symbol).order_by('-published_at')
        response = [
            {
                "title": entry.title,
                "sentiment": entry.sentiment,
                "published_at": entry.published_at,
            }
            for entry in news
        ]
        return Response(response)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['GET'])
def get_recommendation(request, symbol):
    try:
        recommendation = generate_recommendation(symbol)
        return Response({"symbol": symbol, "recommendation": recommendation})
    except Exception as e:
        return Response({"error": str(e)}, status=500)
