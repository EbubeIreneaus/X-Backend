from django.contrib import admin
from .models import  Tweet, TweeetFile, Comment, Like
# Register your models here.

admin.site.register(Tweet)
admin.site.register(TweeetFile)
admin.site.register(Comment)
admin.site.register(Like)