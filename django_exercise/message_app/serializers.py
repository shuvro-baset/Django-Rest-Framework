from authentication_app.models import User
from authentication_app.serializers import UserSerializer
from rest_framework import serializers, status
from rest_framework.response import Response
from message_app.models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'message', 'create_by', 'created_at', 'modified_at',)

    def create(self, validated_data):
        return super(MessageSerializer, self).create(validated_data)

    def validate(self, validated_data):
        return super(MessageSerializer, self).validate(validated_data)
