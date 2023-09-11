from django.urls import path
from . import views
urlpatterns = [
	path('getUserData/<int:id>', views.get_user_data),
	path('toggleFollowing/', views.toogle_following),
	path('getProfile/<int:id>', views.get_profile)
]