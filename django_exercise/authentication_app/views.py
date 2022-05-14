from django.contrib.auth import authenticate
from django.db import transaction
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication_app.models import User
from authentication_app.serializers import UserSerializer, TokenSerializer
from django.http import Http404


class Signout(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class UserRegisterView(APIView):
    activation_email_template = "account_activation_email.html"

    @transaction.atomic
    def post(self, request):
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
        serializer = UserSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()

            # Here need to update don't delete those line
            email_res = User.send_signup_mail(email, self.activation_email_template)
            if email_res != True:
                return Response(email_res, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActiveAccount(APIView):
    # throttle_classes = (AnonRateThrottle,)
    permission_classes = (AllowAny,)

    @csrf_exempt
    def post(self, request, format=None):
        security_code = request.data.get('security_code')
        user = User.objects.filter(security_code=security_code).first()

        if user is not None:
            if user.is_active is not False:
                return Response({'error': 'This user already active.'}, status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                user.is_active = True
                user.save()
                token, created = Token.objects.get_or_create(user=user)
                user.security_code = None
                user.save()
            email_res = User.send_active_universal_code_mail(user.username)
            if email_res != True:
                return Response(email_res, status=status.HTTP_400_BAD_REQUEST)
            response = {
                "message": "Account successfully activated.",
                'user': user.as_json(),
                "success": True
            }
            return Response(response, status=status.HTTP_200_OK)

        else:
            response = {
                "message": "Invalid security code or Session expired.",
                "success": False
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ObtainAuthToken(ObtainAuthToken):
    serializer_class = TokenSerializer
    http_method_names = ['post']
    permission_classes = (AllowAny,)

    @csrf_exempt
    def post(self, request):
        data = {
            "username": request.data.get('email', None),
            "password": request.data.get('password', None),
        }
        print(data)
        authentication = authenticate(request, username=data['username'], password=data['password'])
        if authentication:
            user = User.objects.filter(email=data['username']).first()
            if user is None:
                return Response({"error": "user not found.", "logged_in": False}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"logged_in": True, "data": user.as_json()}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "user not found or wrong password ."}, status=status.HTTP_400_BAD_REQUEST)


class ForgetPasswordView(APIView):
    permission_classes = ()
    authentication_classes = ()

    def get_user_obj(self, email):
        try:
            user = User.objects.get(username=email)
            return user
        except User.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        email = request.data.get("email", None)
        if email is None:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)
        user = self.get_user_obj(email)
        serializer = ForgotPasswordTokenSerializer(user, data={}, partial=True)
        if serializer.is_valid():
            serializer.save()

            # sending Mail
            subject = 'Intello: Reset Password.'
            email_body = "<strong> Hello ! </strong> " \
                         "<p>You’ve requested to reset your password. Use This code for reset your password." \
                         "</p> CODE:   <strong>" + str(serializer.data['security_code']) + "</strong><p> Thank you </p>"
            mailer = Mailer()
            response = mailer.send_email(recipient=email, subject=subject, html_message=email_body)

            if not response:
                return Response({'error': 'Email sending process failed. Please try again'},
                                status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = ResetPasswordSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data, partial=False)
        if serializer.is_valid():
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def patch(self, request, format=None):

        req_user = request.user
        password = request.data.get('new_password')
        if not password:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        trim_pass = password.strip()
        if trim_pass == '':
            return Response(status=status.HTTP_400_BAD_REQUEST)

        req_user.set_password(raw_password=trim_pass)
        req_user.save()
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
