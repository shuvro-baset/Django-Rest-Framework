from django.db import transaction
from rest_framework import serializers
from sqlite3.dbapi2 import IntegrityError

from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import status
from rest_framework.response import Response

from authentication_app.models import User


class TokenSerializer(AuthTokenSerializer):
    pass


class UserSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'password', 'first_name', 'last_name')

        extra_kwargs = {'password': {'write_only': True}}

    def get_email(self, obj):
        return obj.username

    def create(self, validated_data):
        initial_data = self.initial_data
        email = initial_data.get('email')
        password = initial_data.get('password')
        first_name = initial_data.get('first_name')
        last_name = initial_data.get('last_name')

        if User.validate_unique_email(email):
            raise serializers.ValidationError({'email': 'This email already exists.'}, code='error')

        extra_fields = {
            'first_name': first_name,
            'last_name': last_name,
        }

        user = User._create_user(email, password, **extra_fields)
        return user


class ForgotPasswordTokenSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email')  # name or username ?

    def get_id(self, obj):
        return obj.id

    def get_email(self, obj):
        return obj.username


class ResetPasswordSerializer(serializers.Serializer):
    verification_code = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(
        required=True,
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False, write_only=True
    )

    @transaction.atomic
    def validate(self, attrs):

        verification_code = attrs.get('verification_code')
        password = attrs.get('password')

        if verification_code and password:
            user = User.objects.filter(verification_code=verification_code).first()

            # user = student if student is not None else teacher

            if not user:
                return Response(status=status.HTTP_409_CONFLICT)
            else:
                user.set_password(raw_password=password)
                user.save()

                db_transaction = transaction.savepoint()
                user.save()

                try:
                    transaction.savepoint_commit(db_transaction)
                except IntegrityError:
                    transaction.savepoint_rollback(db_transaction)
        else:
            msg = 'Must include "verification_code" and "password".'
            raise serializers.ValidationError(msg, code='error')

        return attrs
