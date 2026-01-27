from django.urls import path

from weddingmanagement.app_customer import views


app_name="app_customer"
urlpatterns = [
    path("servicev/",views.serviceview,name='servicev'),
    path("categoryv/",views.categoryview,name='categoryv'),
    path('price/<int:service_id>/', views.pricedetails, name='price'),


]

