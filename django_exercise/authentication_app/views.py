from django.contrib.auth import authenticate
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from authentication_app.models import User
from authentication_app.serializers import UserSerializer, TokenSerializer


# signout view
class Signout(APIView):
    # restrict user for authentication
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        # delete token when user logged out
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


# user Register view
class UserRegisterView(APIView):

    @transaction.atomic
    def post(self, request):
        # recieving data from user
        email = request.data.get('email', None).lower()
        password = request.data.get('password', None)
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')

        data = {
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
        }
        # pass data to the user serializer
        serializer = UserSerializer(data=data, context={'request': request})
        # validation
        if serializer.is_valid():
            # save user data
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# login view
class ObtainAuthToken(ObtainAuthToken):
    serializer_class = TokenSerializer
    http_method_names = ['post']
    permission_classes = (AllowAny,)

    @csrf_exempt
    def post(self, request):
        data = {
            "username": request.data.get('username', None),
            "password": request.data.get('password', None),
        }
        print(data)
        authentication = authenticate(request, username=data['username'], password=data['password'])
        if authentication:
            user = User.objects.filter(username=data['username']).first()
            if user is None:
                return Response({"error": "user not found.", "logged_in": False}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"logged_in": True, "data": user.as_json()}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "user not found or wrong password ."}, status=status.HTTP_400_BAD_REQUEST)
