from django.urls import path
from app_vendor import views

app_name="app_vendor"
urlpatterns = [
path("staff/",views.staff_view,name='staff'),
path("stafftable/",views.staffv,name='stafftable'),
# path("services/",views.service,name='services'),
path("sdetails/",views.servicedetails,name='sdetails'),
path('gallery/', views.gallery, name='gallery'),
path('gallerytable/', views.gallery_table, name='gallery_table'),
    
]