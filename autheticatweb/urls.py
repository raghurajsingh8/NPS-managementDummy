from django.urls import path
from autheticatweb import views
from django.urls import path
from .views import manage_users, delete_user

from .views import return_item_view,returned_items_list

urlpatterns = [
    path('', views.home, name='home'),
       

    path('login/', views.loginu, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logouthandle, name='logout'),
    path('sale/', views.sale_form, name='sale_form'),
    path('purchase/', views.purchase_form, name='purchase_form'),
    path('dashboard/', views.dashboard, name='dashboard'),
      path('manage-users/', manage_users, name='manage_users'),
    path('delete-user/<int:user_id>/', delete_user, name='delete_user'),
    path('collections/', views.collections, name='collections'),
    path('add_category/', views.add_category, name='add_category'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('add_product/', views.add_product, name='add_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('add_measurement_unit/', views.add_measurement_unit, name='add_measurement_unit'),
    path('delete_measurement_unit/<int:unit_id>/', views.delete_measurement_unit, name='delete_measurement_unit'),
        path('return-item/', return_item_view, name='return_item'),
        path('returned-items/', views.returned_items_list, name='returned-items'),  # This must match

        path('delete-returned-item/<int:item_id>/', views.delete_returned_item, name='delete_returned_item'),
        path('superchart/', views.superchart_view, name='superchart_view'),

 
     
     
      # Add this

   
      # Success page after return creation
]

from django.conf.urls import handler404, handler403
from django.urls import path
from . import views

# Define custom error views
handler404 = 'autheticatweb.views.page_not_found'
handler403 = 'autheticatweb.views.permission_denied'
handler405 = 'autheticatweb.views.method_not_allowed'


