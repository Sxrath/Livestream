# streaming_app/serializers.py
from rest_framework import serializers
from .models import Stream, Report, Chat,User,UserProfile
from django.contrib.auth import authenticate

class StreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stream
        fields = ['title','description','category','is_exclusive']

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = "__all__"

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password','email']

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
        


class CreateUserprofileSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserProfile
        fields=['profile_picture','bio','links']


class UserprofileSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserProfile
        fields='__all__'



class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stream
        fields = []


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserProfile
        fields=[]

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserProfile
        fields=[]
