from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
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
