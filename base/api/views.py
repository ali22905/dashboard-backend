from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import ProfileSerializer, UserSerializer
from django.contrib.auth.models import User
from base.models import Profile

from django.contrib.auth.forms import UserCreationForm



# from this 2 classes you can return whatever data about the user to the frontend
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add the data about the user that you want to return to the frontend
        user_profile = user.profile
        serialized_profile = ProfileSerializer(user_profile)
        print(serialized_profile)
        
        token['username'] = user.username
        token['email'] = user.email
        token['firstname'] = serialized_profile.data.get('firstname')
        token['lastname'] = serialized_profile.data.get('lastname')
        token['phone'] = serialized_profile.data.get('phone')
        token['address1'] = serialized_profile.data.get('address1')
        token['city'] = serialized_profile.data.get('city')
        token['access_level'] = serialized_profile.data.get('access_level')
        token['created'] = serialized_profile.data.get('created')
        # ...

        return token
# make a custom TokenObtainPairView that return the data to the frontend
class MyTokenObtainPairView(TokenObtainPairView):
  serializer_class = MyTokenObtainPairSerializer




# a documentation for the API
@api_view(['GET'])
def getRoutes(request):
  routes = [
    '/api/token',
    '/api/token/refresh',
    '/api/get_users',
    '/api/add_user',
    '/api/get_user/id',
    '/api/update_profile/id',
  ]
  
  
  # safe = false    will make it not necessary to be serilaized (wrong if you are talking with some DB)
  return Response(routes)


@api_view(['GET'])
def getUsers(request):
  users = User.objects.order_by('id')
  serialized_users = UserSerializer(users, many=True)
  return Response(serialized_users.data)


@api_view(['GET'])
def get_user(request, pk):
  profile = Profile.objects.get(user=pk)
  serialized_profile = ProfileSerializer(profile)
  return Response(serialized_profile.data)



@api_view(['GET'])
def get_profiles(request):
  profiles = Profile.objects.order_by('user_id')
  serialized_profile= ProfileSerializer(profiles, many=True)
  return Response(serialized_profile.data)



@api_view([ 'POST'])
def add_user(request):
  if request.method == 'POST':

    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if username and password:
      # Create a new user
      user = User.objects.create_user(username=username, password=password, email=email)
      return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    else:
      return Response({'error': 'Used username or Invalid password'}, status=status.HTTP_400_BAD_REQUEST)



@api_view([ 'POST' ])
def update_profile(request, pk):
  instance = get_object_or_404(Profile, user=pk)

  if Profile.objects.get(user=pk):
    data = request.data.copy() 
    data['user'] = pk
    # data['id'] = instance.id
    serialized_profile = ProfileSerializer(instance, data)

    if serialized_profile.is_valid():
      
      serialized_profile.save()
      return Response({'serilzed_data': serialized_profile.data, 'data_entered': data})
    
    else: 
      return Response({'error': 'Invalid data', 'type': serialized_profile.errors}, status=status.HTTP_400_BAD_REQUEST)
  else:
    return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def delete_user(request, pk):
  try:
    user = User.objects.get(id=pk)
    deleted_user = user
    user.delete()
    return Response({'deleted_user': deleted_user}, status=status.HTTP_200_OK)
  except User.DoesNotExist:
    return Response({'error': "Can't find the given user"}, status=status.HTTP_404_NOT_FOUND)



