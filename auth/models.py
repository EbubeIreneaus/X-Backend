from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
     user =  models.ForeignKey(User, on_delete=models.CASCADE)
     name = models.CharField(max_length=30, default="")
     profile_pics = models.ImageField(upload_to='profile/', null=True)
     date_joined = models.DateField(auto_now_add=True)

     def __str__(self):
          return self.name