from django.urls import path
from . import views
urlpatterns = [
	path('', views.TweetView.as_view()),
	path('<int:id>', views.get_profile_tweet),
	path('likedTweet/<int:id>', views.get_liked_tweet),
	path('repliedTweet/<int:id>', views.get_replied_tweet),
	path('toogleLikeTweet/', views.toogleLikeTweet),
	path('replyTweet/', views.reply_tweet),
	path('getTweet/<int:id>', views.get_single_tweet),
	path('toogleLikeComment/', views.toogle_like_comment),
	path('replyComment/', views.reply_comment),
	path('getComment/<int:id>', views.get_comment)
	]