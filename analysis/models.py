from django.db import models

# Create your models here.

class ETFData(models.Model):
    symbol = models.CharField(max_length=10)
    date = models.DateField()
    open_price = models.FloatField()
    close_price = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    volume = models.BigIntegerField()
    sma_20 = models.FloatField(null=True, blank=True)
    sma_50 = models.FloatField(null=True, blank=True)

class NewsSentiment(models.Model):
    etf_symbol = models.CharField(max_length=10)
    title = models.TextField()
    sentiment = models.CharField(max_length=10)
    published_at = models.DateTimeField()