from rest_framework import serializers
from auth.models import Profile

class ProfileSerialization(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"