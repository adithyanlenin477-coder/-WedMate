from django.urls import path
from app_vendor import views

app_name="app_vendor"
urlpatterns = [
path("staff/",views.staff_view,name='staff'),
path("stafftable/",views.staffv,name='stafftable'),
# path("services/",views.service,name='services'),
path("sdetails/",views.servicedetails,name='sdetails'),
path('payments/', views.vendor_payment_list, name='vendor_payments'),
path('galleryform/', views.gallery, name='gallery'),
path('gallery/', views.gallery_table, name='gallery_table'),
path('gallery/add/', views.gallery, name='gallery_add'),
path('gallery/edit/<int:id>/', views.gallery_edit, name='gallery_edit'),
path('gallery/delete/<int:id>/', views.gallery_delete, name='gallery_delete'),
path('bookings/', views.vendor_bookings, name='vendor_bookings'),
    
]