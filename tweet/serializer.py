from rest_framework import serializers
from .models import Tweet, TweeetFile, Comment, Like
from django.contrib.auth.models import User
from auth.models import Profile, Follow


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'username']


class LikeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Like
		fields = ['user', 'tweetId']


class ProfileFollowerSerializer(serializers.ModelSerializer):
	user = UserSerializer()

	class Meta:
		model = Profile
		fields = "__all__"

class FollowSerializer(serializers.ModelSerializer):
	my_profile = ProfileFollowerSerializer()
	class Meta:
		model = Follow
		fields = "__all__"

class ProfileSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	followers = FollowSerializer(many=True)
	class Meta:
		model = Profile
		fields = "__all__"


class MediaSerializer(serializers.ModelSerializer):
	class Meta:
		model = TweeetFile
		fields = "__all__"


class CommentReplySerializer(serializers.ModelSerializer):
	profile = ProfileSerializer()
	media = MediaSerializer(many=True)
	likes = LikeSerializer(many=True)

	class Meta:
		model = Comment
		fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
	profile = ProfileSerializer()
	media = MediaSerializer(many=True)
	likes = LikeSerializer(many=True)
	replies = serializers.SerializerMethodField()
	class Meta:
		model = Comment
		fields = '__all__'

	# replies = serializers.SerializerMethodField()

	def get_replies(self, obj):
		# Assuming you want to serialize replies as a list of Comment objects
		replies = Comment.objects.filter(replies=obj)
		return CommentReplySerializer(replies, many=True).data


class TweetSerializer(serializers.ModelSerializer):
	media = MediaSerializer(many=True)
	profile = ProfileSerializer()
	likes = LikeSerializer(many=True)
	comments = CommentSerializer(many=True)
	class Meta:
		model = Tweet
		fields = "__all__"