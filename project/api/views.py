from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives, send_mail
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


# user creation
@api_view(['POST'])
def register_function(request):
    try:
        username = request.data['username']
        email = request.data['email']
        password = request.data['password']

        user_ins = User(
            username = username,
            email = email
        )

        user_ins.set_password(password)
        user_ins.is_active = False
        user_ins.save()

        send_mail(
            "Account verification",
            "Your verification code is 12345",
            [email],
            fail_silently=False
        )

        return Response({
            'status': status.HTTP_201_CREATED,
            'msg': 'User created seccessfully!'
        })
    
    
    except Exception as error:
        return Response({
            'status':status.HTTP_400_BAD_REQUEST,
            'msg': str(error)
        })


# user verification via email
@api_view(['POST'])
def registration_verification(request):
    try:
        username = request.data['username']
        code = request.data['code']

        if code == '12345':
            user_ins = User.objects.get(username=username)
            user_ins.is_active = True
            user_ins.save()

            print(user_ins.is_active)

            return Response({
                'status': status.HTTP_200_OK,
                'msg': 'Account varified seccessfully!'
            })

        else:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'msg': 'Invalid verification code!'
            })
    
    except Exception as error:
        return Response({
            'status':status.HTTP_400_BAD_REQUEST,
            'msg': str(error)
        })


# change password
@api_view(['POST'])
def change_password(request):
    try:
        username = request.data['username']
        old_password = request.data['old_password']
        new_password = request.data['new_password']

        user = User.objects.get(username=username)

        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()

            return Response({
                'status': status.HTTP_200_OK,
                'msg': 'Password changed seccessfully!'
            })

        else:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'msg': 'Invalid password!'
            })
    
    except Exception as error:
        return Response({
            'status':status.HTTP_400_BAD_REQUEST,
            'msg': str(error)
        })
