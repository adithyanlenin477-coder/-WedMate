from django.urls import path

from weddingmanagement.app_customer import views


app_name="app_customer"
urlpatterns = [
    path("servicev/",views.serviceview,name='servicev'),
    path('price/<int:service_id>/<int:cid>', views.pricedetails, name='price'),
    path('booking', views.book_service, name='booking'),
    path('booking_details_view', views.bookingdetails_view, name='booking_details_view'),
    path('customer/booking_delete/<int:id>/', views.bookingdetail_delete, name='booking_delete'),
    path('bookingtable/', views.booking, name='bookingtable'),
    path("payment/<int:booking_id>/", views.payment_page, name="payment_page"),
    path('event/<int:id>/datetime/', views.event_datetime, name='event_datetime'),
    path('categoryv/<int:id>/', views.categoryview, name='categoryv'),


    


]

