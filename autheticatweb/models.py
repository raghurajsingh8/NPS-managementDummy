from django.db import models
import datetime


# Define measurement units as choices
from django.db import models

class bbt(models.TextChoices):
    YES = 'yes', 'YES'
    NO = 'no', 'NO'
    NOT_APPLICABLE = 'Not Applicable', 'Not Applicable'
   



class MeasurementUnit(models.Model):
    name = models.CharField(max_length=50, unique=True)  # The name of the measurement unit, e.g., 'Nos', 'Meter', 'Kg', etc.

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):

        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.category.name}"

class Sale(models.Model):
    sale_to = models.CharField(max_length=255)
    quantity = models.IntegerField()
    measurement_unit = models.ForeignKey(MeasurementUnit, related_name='sales', on_delete=models.SET_NULL, null=True, blank=True)  # ForeignKey to MeasurementUnit
    product = models.ForeignKey(Product, related_name='sales', on_delete=models.CASCADE)
    category = models.CharField(max_length=100, blank=True, null=True)
    serial_no = models.CharField(max_length=255)
    box_type = models.CharField(
        max_length=50,
        choices=bbt.choices,  # Use the predefined choices
        default=bbt.YES  # Set default value to "Nos"
    )
    date = models.DateField(default=datetime.date.today)  # Default to today's date
    verified_by = models.CharField(max_length=255)
    description = models.CharField(max_length=255, default='Thankyou')

    rms_id = models.CharField(max_length=255, blank=True, null=True, default=None)

    def save(self, *args, **kwargs):
        if self.product:
            self.category = self.product.category.name
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.sale_to} - {self.product.name}"

class Purchase(models.Model):
    purchased_from = models.CharField(max_length=255)
    quantity = models.IntegerField()
    measurement_unit = models.ForeignKey(MeasurementUnit, related_name='purchases', on_delete=models.SET_NULL, null=True, blank=True)  # ForeignKey to MeasurementUnit
    product = models.ForeignKey(Product, related_name='purchases', on_delete=models.CASCADE)
    category = models.CharField(max_length=100, blank=True, null=True)
    serial_no = models.CharField(max_length=255)
    box_type = models.CharField(
        max_length=50,
        choices=bbt.choices,  # Use the predefined choices
        default=bbt.YES  # Set default value to "Nos"
    )
    date = models.DateField(default=datetime.date.today)  # Default to today's date
    verified_by = models.CharField(max_length=255)
    description = models.CharField(max_length=255, default='Thankyou')
    rms_id = models.CharField(max_length=255, blank=True, null=True, default=None)


    def save(self, *args, **kwargs):
        if self.product:
            self.category = self.product.category.name
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.purchased_from} - {self.product.name}"


class ReturnedItem(models.Model):
    serial_no = models.CharField(max_length=255, unique=False)  # Ensure unique serial numbers
    returned_on = models.DateTimeField(auto_now_add=True)  # Auto record return time

    def __str__(self):
        return f"Serial No: {self.serial_no} - Returned On: {self.returned_on}"



# views.py
from django.shortcuts import render
from .models import Purchase, Sale, Product
from django.db.models import Sum
import datetime

def superchart_view(request):
    # Chart 1: Total Purchased, Total Sales, Remaining Items
    total_purchased = Purchase.objects.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
    total_sales = Sale.objects.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
    remaining_items = total_purchased - total_sales

    # Chart 2: Date Wise Purchase and Sale
    purchases_by_date = Purchase.objects.values('date').annotate(total_purchase=Sum('quantity')).order_by('date')
    sales_by_date = Sale.objects.values('date').annotate(total_sale=Sum('quantity')).order_by('date')

    # Chart 3: Verified By Wise Purchase and Sale
    purchases_by_verified = Purchase.objects.values('verified_by').annotate(total_purchase=Sum('quantity')).order_by('verified_by')
    sales_by_verified = Sale.objects.values('verified_by').annotate(total_sale=Sum('quantity')).order_by('verified_by')

    # Chart 4: Category Wise Purchase and Sale
    purchases_by_category = Purchase.objects.values('category').annotate(total_purchase=Sum('quantity')).order_by('category')
    sales_by_category = Sale.objects.values('category').annotate(total_sale=Sum('quantity')).order_by('category')

    # Pass data to the template
    return render(request, 'Superchart.html', {
        'total_purchased': total_purchased,
        'total_sales': total_sales,
        'remaining_items': remaining_items,
        'purchases_by_date': purchases_by_date,
        'sales_by_date': sales_by_date,
        'purchases_by_verified': purchases_by_verified,
        'sales_by_verified': sales_by_verified,
        'purchases_by_category': purchases_by_category,
        'sales_by_category': sales_by_category,
    })
