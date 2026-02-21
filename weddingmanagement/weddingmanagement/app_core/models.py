from django.db import models

# Create your models here.
class District(models.Model):
    name=models.CharField()
class Location(models.Model):
    name=models.CharField()
    district=models.ForeignKey(District,on_delete=models.CASCADE)
class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    image=models.ImageField(upload_to="media/",null=True)
class Eventtype(models.Model):
    name=models.CharField()
    description=models.CharField()
    image=models.ImageField(upload_to="media/",null=True)    
        

    