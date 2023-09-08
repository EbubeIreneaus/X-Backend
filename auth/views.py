from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse, HttpResponse
from django.core.mail import EmailMultiAlternatives
import re
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Profile
import random

def sanitize(str):
	str = re.sub("[<$#@!&*?>]", '', str)
	return str

def check_username(request):
	if request.method == 'GET':
		username = request.GET['username']
		res = User.objects.filter(username=username).exists()
		return HttpResponse(res)


# Create your views here.
class Auth(APIView):
	def	post(self, request):
		name = sanitize(request.POST['name'])
		email = request.POST['email']
		psw = request.POST['psw']
		username = request.POST['username']
		img = request.FILES.get('img', 'none')

		if username !='' or email !='' or name !='' or psw !='':
			user = User.objects.create_user(username=username, email=email, password=psw)
			if user.id:
				profile = Profile.objects.create(user=user, name=name)
				if img != 'none':
					profile.profile_pics = img
					profile.save()
				return JsonResponse({'status':'success', 'userId':user.id})
			return JsonResponse({'status': 'failed', 'code':'could not create user'})
		return JsonResponse({'status': 'failed', 'code': 'invalid data'})
	def get(self, request):
		username = request.GET['username']
		psw = request.GET['psw']
		user = authenticate(username=username, password=psw)
		if user is not None:
			return JsonResponse({'status':'success', 'userId':user.pk})
		return JsonResponse({'status': 'failed'})

# send verification Email code

def verify_mail(request):
	code = random.randint(100000, 999999)
	if request.method == 'GET':
		email = request.GET['email']
		msg = EmailMultiAlternatives()
		msg.to = [email]
		msg.subject = 'X account verification'
		msg.body = 'Your six(6) digit email verification code is {}'.format(code)
		msg.attach_alternative('<h2>Your Six(6) digit verification code is </h2><p><b>{}</b></p>'.format(code),
							   'text/html')
		if msg.send(fail_silently=False):
			return JsonResponse({'status':'success', 'code': code})
		return JsonResponse({'status': 'failed'})
	return HttpResponse('invalid request method')
