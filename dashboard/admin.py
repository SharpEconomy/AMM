from django.contrib import admin

from .models import OpportunityLog, PriceSnapshot


@admin.register(PriceSnapshot)
class PriceSnapshotAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "uniswap_price", "bitmart_price", "coinstore_price")
    ordering = ("-timestamp",)


@admin.register(OpportunityLog)
class OpportunityLogAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "delta_percent", "uniswap_price", "average_price")
    ordering = ("-timestamp",)
