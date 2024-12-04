from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import fetch_and_save_data, calculate_sma, fetch_and_analyze_news, generate_recommendation

@api_view(['GET'])
def analyze_etf(request, symbol):
    fetch_and_save_data(symbol)
    calculate_sma(symbol)
    fetch_and_analyze_news(symbol)
    recommendation = generate_recommendation(symbol)
    return Response({"symbol": symbol, "recommendation": recommendation})
