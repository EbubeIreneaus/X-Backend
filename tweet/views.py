import json

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework.views import APIView
from.models import Tweet, Comment, TweeetFile,Like
from .serializer import  TweetSerializer, CommentSerializer
from django.http import HttpResponse, JsonResponse
from auth.models import Profile
import re
import mimetypes


def sanitize(str):
	str = re.sub("[<$#@!&*?>]", '', str)
	return str


class TweetView(APIView):
	@transaction.atomic
	def post(self, request):

		profile = Profile.objects.get(user__id=request.headers.get('userId'))
		tweet_txt = re.sub('/[<>]/','',request.POST.get('tweet', ''))
		if tweet_txt == 'null':
			tweet_txt = ''

		medias = request.FILES.getlist('files','')
		try:
			tweet = Tweet(profile=profile, tweet_txt=tweet_txt)
			tweet.save()
			if len(medias) >0:
				for file in medias:
					mime_type, _ = mimetypes.guess_type(file.name)
					if mime_type and mime_type.startswith('image'):
						file = TweeetFile(file=file, type='img')
					# elif mime_type and mime_type.startswith('video'):
					# 	file = TweeetFile(file=file, type='vid')
					file.save()
					tweet.media.add(file)
			tweet.save()
			return JsonResponse({'status':'success'})
		except Exception as e:
			return JsonResponse({'status': 'failed', 'code':str(e)})

	def get(self, request):
		tweet = Tweet.objects.order_by('-id').all()
		stw = TweetSerializer(tweet, many=True)
		return JsonResponse(stw.data, safe=False)


@csrf_exempt
def toogleLikeTweet(request):
	if request.method == 'POST':
		userId = request.headers.get('userId','')
		data = json.loads(request.body)
		try:
			tweet = Tweet.objects.get(pk=data['tweetId'])
			user = User.objects.get(id=userId)
			if data['query'] == "like":
				like = Like.objects.create(user = user, tweetId=data['tweetId'])
				tweet.likes.add(like)
				tweet.save()
			else:
				like = Like.objects.get(user=user, tweetId=data['tweetId'])
				like.delete()
			return  JsonResponse({'status':'success'})
		except Exception as e:
			return JsonResponse({'status': 'failed', 'code':str(e)})

@csrf_exempt
def reply_tweet(request):
	if request.method == 'POST':
		tweetId =  sanitize(request.POST.get('tweetId'))
		medias = request.FILES.getlist('files', '')
		tweet_txt = sanitize(request.POST.get('comment', ''))
		try:
			profile = Profile.objects.get(user__id = request.headers.get('userId',''))
			tweet = Tweet.objects.get(id = tweetId)
			comment = Comment(profile=profile, tweet_txt=tweet_txt)
			comment.save()
			if len(medias) > 0:
				for file in medias:
					mime_type, _ = mimetypes.guess_type(file.name)
					if mime_type and mime_type.startswith('image'):
						file = TweeetFile(file=file, type='img')
					elif mime_type and mime_type.startswith('video'):
						file = TweeetFile(file=file, type='vid')
					file.save()
					comment.media.add(file) #add media to comment					comment.save(
			tweet.comments.add(comment) #add comment to tweet			return JsonResponse({'status': 'success'})
		except Exception as e:
			return JsonResponse({'status': 'failed', 'code': str(e)})

def get_single_tweet(request, id):
	tweet = Tweet.objects.get(id = id)
	stw = TweetSerializer(tweet)
	return JsonResponse(stw.data, safe=False)

@csrf_exempt
def toogle_like_comment(request):
	if request.method == "POST":
		data = json.loads(request.body)
		query = data['query']
		userId = request.headers.get('userId', '')
		commentId = data['commentId']
		try:
			user = User.objects.get(pk=userId)
			comment = Comment.objects.get(pk = commentId)
			if query == "like":
				like = Like.objects.create(user = user, tweetId=commentId)
				comment.likes.add(like)
				comment.save()
			else:
				like = Like.objects.filter(user=user, tweetId=commentId)
				like.delete()
			return JsonResponse({'status':'success'})

		except Exception as e:
			return JsonResponse({'status': 'failed', 'code':str(e)})


@csrf_exempt
def reply_comment(request):
	if request.method == 'POST':
		commentId = sanitize(request.POST.get('commentId'))
		medias = request.FILES.getlist('files', '')
		comment_txt = sanitize(request.POST.get('comment_txt', ''))
		try:
			profile = Profile.objects.get(user__id=request.headers.get('userId', ''))
			comment = Comment.objects.get(id=commentId)
			reply = Comment.objects.create(profile=profile, tweet_txt=comment_txt)

			if len(medias) > 0:
				for file in medias:
					mime_type, _ = mimetypes.guess_type(file.name)
					if mime_type and mime_type.startswith('image'):
						file = TweeetFile(file=file, type='img')
					# elif mime_type and mime_type.startswith('video'):
					# 	file = TweeetFile(file=file, type='vid')
					file.save()
					reply.media.add(file)  # add media to comment
					reply.save()
			comment.replies.add(reply)  # add comment to tweet
			return JsonResponse({'status': 'success'})
		except Exception as e:
			return JsonResponse({'status': 'failed', 'code': str(e)})


def get_comment(request, id):
	comment = Comment.objects.get(id=id)
	comment_serialize = CommentSerializer(comment)
	return JsonResponse(comment_serialize.data, safe=False)


def get_profile_tweet(request, id):
	tweet = Tweet.objects.order_by('-id').filter(profile__user__id=id)
	stw = TweetSerializer(tweet, many=True)
	return JsonResponse(stw.data, safe=False)

def get_liked_tweet(request, id):
	tweet = Tweet.objects.order_by('-id').filter(likes__user__id=id)
	stw = TweetSerializer(tweet, many=True)
	return JsonResponse(stw.data, safe=False)


def get_replied_tweet(request, id):
	tweet = Tweet.objects.order_by('-id').filter(comments__profile__user__id=id)
	stw = TweetSerializer(tweet, many=True)
	return JsonResponse(stw.data, safe=False)