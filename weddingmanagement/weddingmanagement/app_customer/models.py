from django.db import models

from app_core.models import Category
from weddingmanagement.users.models import User

class Gallery(models.Model):
    image=models.ImageField(upload_to="media/",null=True)
    vendor=models.ForeignKey(User, on_delete=models.CASCADE)
    service=models.ForeignKey(Category, on_delete=models.CASCADE)
