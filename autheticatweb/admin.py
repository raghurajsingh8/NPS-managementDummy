from django.contrib import admin
from .models import MeasurementUnit, Product, Sale, Purchase, Category, ReturnedItem

admin.site.register(MeasurementUnit)
admin.site.register(Product)
admin.site.register(Sale)
admin.site.register(Purchase)
admin.site.register(Category)
admin.site.register(ReturnedItem)
