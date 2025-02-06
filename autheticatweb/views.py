from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SaleForm, PurchaseForm
from .models import Sale, Purchase
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User  # Add this import for User model
import re
# Home view
def home(request):
    return render(request, 'home.html')
def custom_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You must log in first to access this page.")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper
# Login view
def loginu(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['pass1']
        remember_me = request.POST.get('remember_me')  # Capture remember me checkbox value
  # Get remember me checkbox value

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if remember_me:
                request.session.set_expiry(60 * 60 * 24 * 30)  # Set session expiration to 30 days
            return redirect('home')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')
    return render(request, 'login.html')

# Signup view
def signup(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['pass1']
        confirm_password = request.POST['pass2']
        if password != confirm_password:
            messages.warning(request, "Password is not matching")
            return render(request, 'signup.html')
        try:
            if User.objects.get(username=email):
                messages.info(request, "Email is taken")
                return render(request, 'signup.html')
        except User.DoesNotExist:
            pass
        user = User.objects.create_user(username=email, email=email, password=password)
        user.save()
        messages.success(request, "Registration Successful")
        return redirect('login')
    return render(request, 'signup.html')

# Logout view
def logouthandle(request):
    logout(request)
    messages.info(request, "Logout Success")
    return redirect('login')

# Sale form view
@custom_login_required
def sale_form(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            # Get the serial numbers from the form
            serial_no = form.cleaned_data['serial_no']
            # Split the serial numbers by commas or new lines
            serial_no_list = [serial.strip() for serial in serial_no.split(',')]  # Or use split('\n') for new lines

            # Loop over the list and create individual Sale records for each serial number
            for serial in serial_no_list:
                # Create a new Sale object for each serial number
                sale = Sale(serial_no=serial)  # Create a new Sale instance with the serial number
# Assign the individual serial number
                sale.save()  # Save the individual Sale record

            return redirect('dashboard')  # Redirect to the list or success page
    else:
        form = SaleForm()
    return render(request, 'sale_form.html', {'form': form})

# Purchase form view
@custom_login_required
def purchase_form(request):
     if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            # Get the serial numbers from the form
            serial_no = form.cleaned_data['serial_no']
            # Split the serial numbers by commas or new lines
            serial_no_list = [serial.strip() for serial in serial_no.split(',')]

            # Loop over the list and create individual Purchase records for each serial number
            for serial in serial_no_list:
                # Create a new Purchase object for each serial number
             purchase = Purchase(serial_no=serial)  # Create a new Sale instance with the serial number
  # Assign the individual serial number
            purchase.save()  # Save the individual Purchase record

            return redirect('dashboard')  # Redirect to the list or success page
     else:
        form = PurchaseForm()
     return render(request, 'purchase_form.html', {'form': form})

# Dashboard view
@custom_login_required
def dashboard(request):
    sales = Sale.objects.all()
    purchases = Purchase.objects.all()
    return render(request, 'dashboard.html', {'sales': sales, 'purchases': purchases})



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages

# Check if user is a superuser
def superuser_required(view_func):
    return user_passes_test(lambda u: u.is_superuser, login_url='home')(view_func)

@superuser_required
def manage_users(request):
    if not request.user.is_superuser:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('home')  # Redirect to a safe page, e.g., the homepage
    if request.method == "POST":
        # Handle user creation
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        is_admin = request.POST.get('is_admin') == 'on'  # Checkbox for admin status

        if not username or not email or not password:
            messages.error(request, "All fields are required.")
        else:
            try:
                if User.objects.filter(username=username).exists():
                    messages.error(request, "Username already exists.")
                elif User.objects.filter(email=email).exists():
                    messages.error(request, "Email already exists.")
                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    if is_admin:
                        user.is_staff = True
                        user.is_superuser = True
                    user.save()
                    messages.success(request, "User created successfully.")
            except Exception as e:
                messages.error(request, f"Error: {e}")

    # Fetch all users excluding superusers
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'manage_users.html', {'users': users})

@superuser_required
def delete_user(request, user_id):
    
    try:
        user = User.objects.get(id=user_id)
        if user.is_superuser:
            messages.error(request, "You cannot delete another superuser.")
        else:
            user.delete()
            messages.success(request, "User deleted successfully.")
    except User.DoesNotExist:
        messages.error(request, "User does not exist.")
    return redirect('manage_users')


@custom_login_required
def sale_form(request):
    returned_items = ReturnedItem.objects.all()
    returned_serials = set(returned_items.values_list('serial_no', flat=True)) 
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            # Get the serial numbers from the form
            serial_no = form.cleaned_data['serial_no']
            # Split the serial numbers by commas or new lines
            import re

            serial_no_list = [serial.strip() for serial in re.split('[,\n]+', serial_no)]

  # Or use split('\n') for new lines

            # Loop over the list and create individual Sale records for each serial number
            for serial in serial_no_list:
                # Create a new Sale object for each serial number
                sale = Sale(
                    sale_to=form.cleaned_data['sale_to'],
                    quantity=form.cleaned_data['quantity'],
                    measurement_unit=form.cleaned_data['measurement_unit'],
                    product=form.cleaned_data['product'],
                    category=form.cleaned_data['category'],
                    serial_no=serial,  # Use individual serial number
                    box_type=form.cleaned_data['box_type'],
                    date=form.cleaned_data['date'],
                    verified_by=request.user.email,
                    description=form.cleaned_data['description']  # Description ko add kiya

                )
                sale.save()  # Save the individual Sale record

            return redirect('dashboard')  # Redirect to the list or success page
    else:
        form = SaleForm()
    return render(request, 'sale_form.html', {'form': form})

@custom_login_required
def purchase_form(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            # Get the serial numbers from the form
            serial_no = form.cleaned_data['serial_no']
            # Split the serial numbers by commas or new lines
            import re
            serial_no_list = [serial.strip() for serial in re.split('[,\n]+', serial_no)]


            # Loop over the list and create individual Purchase records for each serial number
            for serial in serial_no_list:
                # Create a new Purchase object for each serial number
                purchase = Purchase(
                    purchased_from=form.cleaned_data['purchased_from'],
                    quantity=form.cleaned_data['quantity'],
                    measurement_unit=form.cleaned_data['measurement_unit'],
                    product=form.cleaned_data['product'],
                    category=form.cleaned_data['category'],
                    serial_no=serial,  # Use individual serial number
                    box_type=form.cleaned_data['box_type'],
                    date=form.cleaned_data['date'],
                    verified_by=request.user.email,
                    description=form.cleaned_data['description']  # Description ko add kiya

                )
                purchase.save()  # Save the individual Purchase record

            return redirect('dashboard')  # Redirect to the list or success page
    else:
        form = PurchaseForm()
    return render(request, 'purchase_form.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Product, MeasurementUnit
from django.http import HttpResponse

# Collection page - Display categories, products, and measurement units
@custom_login_required
def collections(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    measurement_units = MeasurementUnit.objects.all()

    return render(request, 'collections.html', {
        'categories': categories,
        'products': products,
        'measurement_units': measurement_units
    })

# Add Category
@custom_login_required
def add_category(request):
    if request.method == 'POST':
        category_name = request.POST['category_name']
        if Category.objects.filter(name=category_name).exists():
            messages.error(request, 'Category already exists!')
        else:
            Category.objects.create(name=category_name)
            messages.success(request, 'Category added successfully!')
    return redirect('collections')

# Delete Category
@login_required
def delete_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        category.delete()
        messages.success(request, 'Category deleted successfully!')
    except Category.DoesNotExist:
        messages.error(request, 'Category not found!')
    return redirect('collections')

# Add Product
@custom_login_required
def add_product(request):
    if request.method == 'POST':
        product_name = request.POST['product_name']
        category_id = request.POST['category']
        category = Category.objects.get(id=category_id)
        if Product.objects.filter(name=product_name, category=category).exists():
            messages.error(request, 'Product already exists in this category!')
        else:
            Product.objects.create(name=product_name, category=category)
            messages.success(request, 'Product added successfully!')
    return redirect('collections')

# Delete Product
@custom_login_required
def delete_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        product.delete()
        messages.success(request, 'Product deleted successfully!')
    except Product.DoesNotExist:
        messages.error(request, 'Product not found!')
    return redirect('collections')

# Add Measurement Unit
@custom_login_required
def add_measurement_unit(request):
    if request.method == 'POST':
        measurement_unit_name = request.POST['measurement_unit_name']
        if MeasurementUnit.objects.filter(name=measurement_unit_name).exists():
            messages.error(request, 'Measurement unit already exists!')
        else:
            MeasurementUnit.objects.create(name=measurement_unit_name)
            messages.success(request, 'Measurement unit added successfully!')
    return redirect('collections')

# Delete Measurement Unit
@custom_login_required
def delete_measurement_unit(request, unit_id):
    try:
        unit = MeasurementUnit.objects.get(id=unit_id)
        unit.delete()
        messages.success(request, 'Measurement unit deleted successfully!')
    except MeasurementUnit.DoesNotExist:
        messages.error(request, 'Measurement unit not found!')
    return redirect('collections')


   
from django.shortcuts import render
from .forms import ReturnItemForm

from .models import ReturnedItem

@custom_login_required
def return_item_view(request):
    
    if request.method == 'POST':
        form = ReturnItemForm(request.POST)
        if form.is_valid():
            serial_no = form.cleaned_data['serial_no']
            # Save the returned item
            ReturnedItem.objects.create(serial_no=serial_no)
            return render(request, 'return_success.html', {'serial_no': serial_no})
    else:
        form = ReturnItemForm()
    return render(request, 'return_item.html', {'form': form})

from django.shortcuts import render


@custom_login_required
def returned_items_list(request):
    # Fetch all serial numbers from the Sale model
    sale_serials = Sale.objects.values_list('serial_no', flat=True)  # Extract only serial numbers
    # Fetch all returned items and order them by return date (descending)
    returned_items = ReturnedItem.objects.all().order_by('-returned_on')  
    return render(request, 'returned_items.html', {
        'returned_items': returned_items,
        'sale_serials': list(sale_serials)  # Pass serial numbers as a list
    })



from django.http import JsonResponse
from .models import ReturnedItem

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import ReturnedItem
@custom_login_required
def delete_returned_item(request, item_id):
    if request.method == 'DELETE':
        item = get_object_or_404(ReturnedItem, id=item_id)
        item.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)



from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import ReturnedItem
from .forms import ReturnItemForm
@custom_login_required
def return_item_view(request):
    sales = Sale.objects.all()

    if request.method == 'POST':
        form = ReturnItemForm(request.POST)
        if form.is_valid():
            serial_no = form.cleaned_data['serial_no']
            # Save the returned item
            ReturnedItem.objects.create(serial_no=serial_no)
            return render(request, 'return_success.html', {'serial_no': serial_no})
    elif request.method == 'DELETE':
        # Get the ID of the item to delete from the request
        item_id = request.POST.get('item_id')
        item = get_object_or_404(ReturnedItem, id=item_id)
        
        # Delete the item
        item.delete()
        
        return JsonResponse({'success': True, 'message': 'Item deleted successfully.'})
    
    else:
        form = ReturnItemForm()
    
    return render(request, 'return_item.html', {'form': form,        'sales': sales,
})
from datetime import datetime, timedelta,date

from .models import Sale, ReturnedItem

from datetime import date, timedelta

def dashboard(request):
    # Get all sales and returned items
    purchases = Purchase.objects.all()  # Renamed to `purchases` for consistency
    sales = Sale.objects.all()
    returned_items = ReturnedItem.objects.all()
    returned_serials = set(returned_items.values_list('serial_no', flat=True))  # Set of returned serial numbers
    sales_serialno = Sale.objects.values_list('serial_no', flat=True)  # Extract serial numbers only
    
    # Handle date filter
    filter_date = request.GET.get('filter_date', 'all')
    today = date.today()

    if filter_date == 'today':
        sales = sales.filter(date=today)
        purchases = purchases.filter(date=today)
    elif filter_date == 'last3days':
        start_date = today - timedelta(days=3)
        sales = sales.filter(date__range=[start_date, today])
        purchases = purchases.filter(date__range=[start_date, today])
    elif filter_date == 'last7days':
        start_date = today - timedelta(days=7)
        sales = sales.filter(date__range=[start_date, today])
        purchases = purchases.filter(date__range=[start_date, today])
    elif filter_date == 'last15days':
        start_date = today - timedelta(days=15)
        sales = sales.filter(date__range=[start_date, today])
        purchases = purchases.filter(date__range=[start_date, today])
    elif filter_date == 'last1month':
        start_date = today - timedelta(days=30)
        sales = sales.filter(date__range=[start_date, today])
        purchases = purchases.filter(date__range=[start_date, today])
    elif filter_date == 'last3months':
        start_date = today - timedelta(days=90)
        sales = sales.filter(date__range=[start_date, today])
        purchases = purchases.filter(date__range=[start_date, today])
    elif filter_date == 'last6months':
        start_date = today - timedelta(days=180)
        sales = sales.filter(date__range=[start_date, today])
        purchases = purchases.filter(date__range=[start_date, today])

    return render(request, 'dashboard.html', {
        'sales': sales,
        'returned_serials': returned_serials,
        'purchases': purchases,  # Updated variable name
        'sales_serialno': sales_serialno
    })



from django.shortcuts import get_object_or_404, redirect

from django.shortcuts import get_object_or_404, redirect

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

def delete_returned_item(request, item_id):
    if request.method == "POST":  # Ensure it is a POST request
        item = get_object_or_404(ReturnedItem, id=item_id)
        item.delete()
        return redirect(reverse('returned-items'))  # Dynamically resolve the URL
    return redirect(reverse('returned-items'))

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

    # Chart 5: Product-wise Purchase and Sale
    purchase_by_product = Purchase.objects.values('product').annotate(total_quantity=Sum('quantity')).order_by('product')
    sale_by_product = Sale.objects.values('product').annotate(total_quantity=Sum('quantity')).order_by('product')
    percentage = (total_sales / total_purchased) * 100 if total_purchased != 0 else 0
    total_products = Purchase.objects.values('product').distinct().count() or 0
    total_categories = Purchase.objects.values('category').distinct().count() or 0

    # Pass data to the template
    return render(request, 'Superchart.html', {
            'percentage': percentage,

        'total_purchased': total_purchased,
        'total_sales': total_sales,
        'remaining_items': remaining_items,
        'purchases_by_date': purchases_by_date,
        'sales_by_date': sales_by_date,
        'purchases_by_verified': purchases_by_verified,
        'sales_by_verified': sales_by_verified,
        'purchases_by_category': purchases_by_category,
        'sales_by_category': sales_by_category,
        'purchases_by_product': purchase_by_product,
        'sales_by_product': sale_by_product,
        'total_products': total_products,
        'total_categories': total_categories,
    })

from django.shortcuts import render
from django.http import HttpResponse

def page_not_found(request, exception):
    return render(request, 'errors/404.html', status=404)

def permission_denied(request, exception):
    return render(request, 'errors/403.html', status=403)

def method_not_allowed(request, exception):
    return render(request, 'errors/405.html', status=405)

from django.http import HttpResponseNotAllowed
from django.shortcuts import render

def method_not_allowed(request, exception):
    return HttpResponseNotAllowed('Method Not Allowed')
def page_not_found(request, exception):
    return render(request, '404.html', status=404)

def permission_denied(request, exception):
    return render(request, '403.html', status=403)

@custom_login_required
def sale_form(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            serial_no = form.cleaned_data['serial_no']
            rms_id = form.cleaned_data.get('rms_id') or None
            serial_no_list = [serial.strip() for serial in re.split('[,\n]+', serial_no)]
            rms_id_list = [rms.strip() for rms in re.split('[,\n]+', rms_id)] if rms_id else [None] * len(serial_no_list)

            for serial, rms in zip(serial_no_list, rms_id_list):
                sale = Sale(
                    sale_to=form.cleaned_data['sale_to'],
                    quantity=form.cleaned_data['quantity'],
                    measurement_unit=form.cleaned_data['measurement_unit'],
                    product=form.cleaned_data['product'],
                    category=form.cleaned_data['category'],
                    serial_no=serial,
                    rms_id=rms,
                    box_type=form.cleaned_data['box_type'],
                    date=form.cleaned_data['date'],
                    verified_by=request.user.email,
                    description=form.cleaned_data['description']
                )
                sale.save()
            return redirect('dashboard')
    else:
        form = SaleForm()
    return render(request, 'sale_form.html', {'form': form})

@custom_login_required
def purchase_form(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            serial_no = form.cleaned_data['serial_no']
            rms_id = form.cleaned_data.get('rms_id') or None
            serial_no_list = [serial.strip() for serial in re.split('[,\n]+', serial_no)]
            rms_id_list = [rms.strip() for rms in re.split('[,\n]+', rms_id)] if rms_id else [None] * len(serial_no_list)

            for serial, rms in zip(serial_no_list, rms_id_list):
                purchase = Purchase(
                    purchased_from=form.cleaned_data['purchased_from'],
                    quantity=form.cleaned_data['quantity'],
                    measurement_unit=form.cleaned_data['measurement_unit'],
                    product=form.cleaned_data['product'],
                    category=form.cleaned_data['category'],
                    serial_no=serial,
                    rms_id=rms,
                    box_type=form.cleaned_data['box_type'],
                    date=form.cleaned_data['date'],
                    verified_by=request.user.email,
                    description=form.cleaned_data['description']
                )
                purchase.save()
            return redirect('dashboard')
    else:
        form = PurchaseForm()
    return render(request, 'purchase_form.html', {'form': form})
