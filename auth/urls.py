from django.urls import path
from . import views


urlpatterns = [
	path('', views.Auth.as_view(), name='auth-auth'),
	path('verifyEmail/', views.verify_mail),
	path('checkUserData/', views.check_username)

]
