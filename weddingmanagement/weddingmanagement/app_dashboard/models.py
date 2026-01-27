from django.db import models

from app_core.models import Category
from weddingmanagement.users.models import User

# Create your models here.
class Vendor(models.Model):

    licenseno=models.CharField()
    phno=models.CharField()
    location=models.CharField()
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=1,related_name="user") 
class VendorService(models.Model):
    vendor = models.ForeignKey(User, on_delete=models.CASCADE,related_name="service_vendor")
    service = models.ForeignKey(Category, on_delete=models.CASCADE,related_name="services")
    amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)

    class Meta:
        unique_together = ('vendor', 'service')

class Customer(models.Model):
    contact=models.CharField()
    address=models.CharField()
    location=models.CharField()
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=1,related_name="customer")     
    