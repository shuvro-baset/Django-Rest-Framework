from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from authentication_app.models import User

# token serializer class
class TokenSerializer(AuthTokenSerializer):
    pass

# user Serializer
class UserSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ( 'id', 'email', 'first_name', 'last_name')

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
