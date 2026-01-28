from django.db import models
from weddingmanagement.users.models import User

# Create your models here.
class Staff(models.Model):
    gender=models.CharField()
    phno=models.CharField()
    location=models.CharField()
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=1,related_name="staff")
    vendor=models.ForeignKey(User,on_delete=models.CASCADE,default=1,related_name="vendor")
