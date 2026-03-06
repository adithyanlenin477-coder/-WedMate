from django.urls import path
from app_core import views

app_name="app_core"
urlpatterns = [
    path("district/",views.district,name="district"),
    path('distview/',views.dis,name='distview'),
    path("location/",views.location,name="location"),
    path('disdelete/<int:id>/', views.disdl, name='disdl'),
    path('disupdate/<int:id>/', views.disup, name='disup'),
    path('locview/',views.locview,name='locview'),
    path("locdl/<int:name>/", views.locdl, name="locdl"),   # delete
    path("locup/<int:name>/", views.locup, name="locup"),   # update
    path("category/",views.category,name="category"),
    path('catview/',views.cat,name='catview'),
    path("catev/", views.catev, name="catv"),
    path("catedl/<int:name>", views.catedl, name="catdl"),
    path("cateup/<int:name>", views.cateup, name="catup"),
    
    
    path("eventtype/",views.eventtype,name="eventtype"),
    path('evntview/',views.evnt,name='evntview'),
    path("evntv/", views.evntv, name="evtv"),
    path("evntdl/<int:name>", views.evntdl, name="evtdl"),
    path("evntup/<int:name>", views.evntup, name="evtup"),
    path("vendorv/", views.vendorview, name="vendrv"),
    path("customertable/",views.custv,name='customertable'),
    path('admin/payments/', views.admin_payment_list, name='admin_payment_list'),
    path('admin_booking_report/', views.admin_booking_report, name='admin_booking_report'),
    path("auditorium/",views.auditorium,name="auditorium"),
    path('auditoriumview/',views.auditoriumview,name='auditoriumview'),
    path("auditoriumdl/<int:id>", views.auditoriumdl, name="auditoriumdl"),
    path("auditoriumup/<int:id>", views.auditoriumup, name="auditoriumup"),
    
    path('get-locations/', views.get_locations, name='get_locations'),
    path('admin_auditorium_report/', views.auditorium_booking_pie_chart, name='admin_auditorium_report'),
    
]