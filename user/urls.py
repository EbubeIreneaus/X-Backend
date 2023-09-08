from django.urls import path
from . import views
urlpatterns = [
	path('getUserData/<int:id>', views.get_user_data)
]