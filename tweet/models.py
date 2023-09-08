from django.db import models
from django.contrib.auth.models import User
from auth.models import Profile
# Create your models here.

class TweeetFile(models.Model):
	file = models.FileField(upload_to="media/")
	type = models.CharField(max_length=5, default='img')

class Like(models.Model):
	user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
	tweetId = models.IntegerField(default=0)
	date = models.DateField(auto_now_add=True)
	
	
class Comment(models.Model):
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
	tweet_txt = models.TextField(null=True)
	media = models.ManyToManyField(TweeetFile, null=True)
	likes = models.ManyToManyField(Like, null=True)
	views = models.IntegerField(default=1)
	date = models.DateField(auto_now_add=True)
	replies = models.ManyToManyField('self', null=True)
	def __str__(self):
		return f'{self.pk} {self.tweet_txt}  {self.date}'
	
	
class Tweet(models.Model):
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
	tweet_txt = models.TextField(null=True)
	media = models.ManyToManyField(TweeetFile, null=True)
	comments = models.ManyToManyField(Comment, null=True)
	likes = models.ManyToManyField(Like, null=True)
	views = models.IntegerField(default=1)
	date = models.DateField(auto_now_add=True)

	def __str__(self):
		return f'{self.pk} {self.tweet_txt}  {self.date}'