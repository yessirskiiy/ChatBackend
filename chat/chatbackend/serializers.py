from rest_framework.serializers import ModelSerializer, ValidationError
from .models import *
from django.contrib.auth.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'is_active', 'first_name', 'last_name']


class DialogSerializer(ModelSerializer):
    class Meta:
        model = Dialog
        fields = '__all__'

    def validate_user(self, value):
        author = self.context['request'].user

        if value == author:
            raise ValidationError("Вы не можете начать диалог с собой")

        return value


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
