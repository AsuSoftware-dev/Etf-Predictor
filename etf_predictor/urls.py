"""
URL configuration for etf_predictor project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from analysis.views import analyze_etf, get_financial_data, get_news_data, get_recommendation
from django.http import HttpResponse

def index(request):
    return HttpResponse("Aplicația funcționează!")

urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
    path('analyze/<str:symbol>/', analyze_etf),
    path('data/<str:symbol>/', get_financial_data),
    path('news/<str:symbol>/', get_news_data),
    path('recommendation/<str:symbol>/', get_recommendation),
]
