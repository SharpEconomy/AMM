from django.db import models


class PriceSnapshot(models.Model):
    timestamp = models.DateTimeField()
    uniswap_price = models.FloatField()
    bitmart_price = models.FloatField(null=True, blank=True)
    coinstore_price = models.FloatField(null=True, blank=True)


class OpportunityLog(models.Model):
    timestamp = models.DateTimeField()
    delta_percent = models.FloatField()
    uniswap_price = models.FloatField()
    average_price = models.FloatField()
