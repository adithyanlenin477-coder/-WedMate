from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models

class User(AbstractUser):
    """
    Default custom user model for WeddingManagement.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255,null=True)
    username=CharField(unique=True)
    password=CharField(unique=True)
    email=models.EmailField(unique=True,default='')
    rolechoices=[('client','client'),('vendors','vendors'),('staff','staff')]
    role=models.CharField(choices=rolechoices,null=False,blank=False,default='admin')
    
    

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
