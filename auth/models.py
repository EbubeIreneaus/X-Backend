from django.db import models
from django.contrib.auth.models import User

class Follow(models.Model):
     my_profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name="follower")
     idol_profile = models.ForeignKey('Profile', on_delete=models.CASCADE)

# Create your models here.
class Profile(models.Model):
     user =  models.ForeignKey(User, on_delete=models.CASCADE)
     name = models.CharField(max_length=30, default="")
     profile_pics = models.ImageField(upload_to='profile/', null=True)
     date_joined = models.DateField(auto_now_add=True)
     followers = models.ManyToManyField(Follow, related_name="followers")
     following = models.ManyToManyField(Follow)

     def __str__(self):
          return self.name