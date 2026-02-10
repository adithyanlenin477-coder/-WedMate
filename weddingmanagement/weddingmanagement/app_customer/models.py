from django.db import models

from app_core.models import Category, Eventtype
from app_dashboard.models import Customer, VendorService
from weddingmanagement.users.models import User

class Gallery(models.Model):
    image=models.ImageField(upload_to="media/",null=True)
    vendor=models.ForeignKey(User, on_delete=models.CASCADE)
    service=models.ForeignKey(Category, on_delete=models.CASCADE)
    
class Booking_master(models.Model):
    customer=models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    booking_date=models.DateField(auto_now_add=True)
    event_date = models.DateField(null=True, blank=True)
    venue=models.CharField(max_length=255)
    number_of_participants = models.IntegerField(null=True, blank=True)
    time=models.TimeField()
    note=models.TextField(blank=True, null=True)
    grandtotal=models.CharField(null=True,blank=True)

class Booking_details(models.Model):
    booking_master=models.ForeignKey(Booking_master, on_delete=models.SET_NULL,   # important
        null=True,
        blank=True, related_name="details")
    service=models.ForeignKey(VendorService, on_delete=models.CASCADE, related_name="bookings_service")
    event=models.ForeignKey(Eventtype, on_delete=models.CASCADE, related_name="bookings_event")
    customer=models.ForeignKey(User,on_delete=models.CASCADE,related_name="booking_customer")

class Payment(models.Model):
    booking = models.ForeignKey(Booking_master, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    
