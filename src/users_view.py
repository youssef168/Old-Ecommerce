#FROM DJANGO
from webbrowser import get
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

# FROM REST
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

#FROM REST_JWT
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import UserSerializer, UserTokenSerialzer


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserTokenSerialzer(self.user).data

        for k,v in serializer.items():
            data[k] = v

        return data
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['message'] = "Message From AlphaShop"

        return token

class MyTokenObainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer


@api_view(['POST'])
def register_view(request):
    data = request.data
    try:
        user = User.objects.create(
            username = data['name'],
            email = data['email'],
            password = make_password(data['password']),
        )

        serializer = UserTokenSerialzer(user,many=False)
        return Response(serializer.data)
    
    except:
        message = {"detail":"User with this email is already registered"}
        return Response(message,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([permissions.IsAdminUser])
def delete_user(request, user_id):
     user = User.objects.get(id=user_id)
     user.delete()
     message = {'message': 'User deleted successfully'}
     return Response(message,status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def search_users(request, name):
    user = User.objects.filter(username__icontains=name)
    serializer = UserSerializer(user, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def get_user_by_id(request, user_id):
    user = User.objects.get(id=user_id)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_profile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_user(request, user_id):
    user  = User.objects.get(id=user_id)
    data = request.data
    user.username = data['name']
    user.email = data['email']
    user.password = make_password(data['password'])
    user.is_staff = data['isAdmin']
    user.save()
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_user_profile(request):
    user = request.user
    serializer = UserTokenSerialzer(user, many=False)
    data = request.data

    user.username = data['name']
    user.email = data['email']
    
    if user.password != '':
        user.password = make_password(data['password'])

    user.save()

    return Response(serializer.data)