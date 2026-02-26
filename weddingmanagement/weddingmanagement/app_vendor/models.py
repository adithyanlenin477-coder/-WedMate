from django.db import models
from app_customer.models import Booking_master
from weddingmanagement.users.models import User

# Create your models here.
class Staff(models.Model):
    gender=models.CharField()
    phno=models.CharField()
    location=models.CharField()
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=1,related_name="staff")
    vendor=models.ForeignKey(User,on_delete=models.CASCADE,default=1,related_name="vendor")

class StaffAssignment(models.Model):
    booking = models.ForeignKey(Booking_master, on_delete=models.CASCADE, related_name="staff_assignments")
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.staff.user.username} → Booking {self.booking.id}"    
