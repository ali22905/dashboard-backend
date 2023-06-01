from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from base.models import Profile

class UserSerializer(ModelSerializer):
  class Meta:
    model = User
    fields = '__all__'


class ProfileSerializer(ModelSerializer):
  class Meta:
    model = Profile
    fields = '__all__'
