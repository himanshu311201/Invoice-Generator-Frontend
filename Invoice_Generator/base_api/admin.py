from django.contrib import admin

# Register your models here.
from django.apps import AppConfig


class StockGameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Stock_Game'