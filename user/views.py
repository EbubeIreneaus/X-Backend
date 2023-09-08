from django.shortcuts import render
from auth.models import Profile
from django.http import HttpResponse, JsonResponse

# Create your views here.
def get_user_data(request, id):
	try:
		profile = Profile.objects.get(user__pk=id)
		return JsonResponse({'status':'success','name':profile.name,'username':profile.user.username,
							 'pics':profile.profile_pics.name})
	except Profile.DoesNotExist:
		return JsonResponse({'status':'failed'})
