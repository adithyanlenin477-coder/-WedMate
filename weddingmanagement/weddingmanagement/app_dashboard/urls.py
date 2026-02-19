from django.urls import path
from app_dashboard import views
from weddingmanagement.app_core import admin

app_name="app_dashboard"
urlpatterns = [
    path("admin/",views.appdash),
    path("",views.guestdash,name='guest'),
    path("login/",views.login_view,name='login'),
    path("registration/",views.reg_view,name='registration'),
    path("vendordash/",views.vendor_dash,name='vendordash'),
    path("staff/",views.staffdash,name='staff'), 
    path("customerreg/",views.customer_view,name='customerreg'),
    path("customerdash/",views.customer_dash,name='customerdash'),
    path('reg/', views.select_role, name="select_role"),
    path('vendor-register/', views.reg_view, name="vendor_register"),
    path('customer-register/', views.customer_view, name="customer_register"),
    path('events/', views.event_list, name='event_list'),
    path('dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
]


