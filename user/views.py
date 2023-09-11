import json

from django.shortcuts import render
from auth.models import Profile, Follow
from django.contrib.auth.models import User
from tweet.serializer import ProfileSerializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def get_user_data(request, id):
	try:
		profile = Profile.objects.get(user__pk=id)
		return JsonResponse({'status':'success','name':profile.name,'username':profile.user.username,
							 'pics':profile.profile_pics.name})
	except Profile.DoesNotExist:
		return JsonResponse({'status':'failed'})

@csrf_exempt
def toogle_following(request):
	if request.method == "POST":
		data = json.loads(request.body)
		personId = data['personId']
		userId = data['userId']
		try:
			idol_profile = Profile.objects.get(pk=personId)
			my_profile = Profile.objects.get(user__id= userId)
			if Follow.objects.filter(idol_profile__id=idol_profile.id,
												 my_profile__id = my_profile.id).count() < 1:
				follow = Follow.objects.create(idol_profile=idol_profile, my_profile=my_profile)
				idol_profile.followers.add(follow)
				my_profile.following.add(follow)
				return JsonResponse({"status":"success", "code":"follow"})
			else:
				follow = Follow.objects.filter(idol_profile__id=idol_profile.id, my_profile__id=my_profile.id)
				follow.delete()
				return JsonResponse({"status": "success", "code": "unfollow"})
		except Exception as e:
			return
			return JsonResponse({"status": "failed", "code":str(e)})

def get_profile(request, id):
	profile = Profile.objects.get(user__id = id)
	serialize_profile = ProfileSerializer(profile)
	return  JsonResponse(serialize_profile.data, safe=False)