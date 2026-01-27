from django.urls import path
from app_core import views

app_name="app_core"
urlpatterns = [
    path("district/",views.district,name="district"),
    path('distview/',views.dis,name='distview'),
    path("location/",views.location,name="location"),
    path("disdl/<int:name>/", views.disdl, name="disdl"),   # delete
    path("disup/<int:name>/", views.disup, name="disup"),   # update
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
]