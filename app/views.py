from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Stream, Report, Chat
from .serializers import SubscriptionSerializer, StreamSerializer,  ReportSerializer, ChatSerializer,UserSerializer,CreateUserprofileSerializer,LikeSerializer,FollowerSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.views import APIView
from .models import UserProfile,User
from django.http import Http404
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class Register(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({"status":403,'errors':serializer.errors,"message":'invalid data'})

        serializer.save()
        user = User.objects.get(username=serializer.data['username'])
        refresh = RefreshToken.for_user(user)

        return Response({"message": "Successfully registered!",   'refresh': str(refresh),
        'access': str(refresh.access_token,)}, status=status.HTTP_201_CREATED)

class LoginView(APIView):

    def post(self, request):
    
        username = request.data.get('username')
        password = request.data.get('password')

        
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                'message': 'Successfully logged in!',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return JsonResponse({
            'message': 'Invalid credentials. Unable to log in.',
        }, status=status.HTTP_401_UNAUTHORIZED)

class CreateProfile(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = CreateUserprofileSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    
class UpdateProfile(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = CreateUserprofileSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
   
class StreamListCreateView(generics.ListCreateAPIView):
    queryset = Stream.objects.all()
    serializer_class = StreamSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class StreamDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Stream.objects.all()
    serializer_class = StreamSerializer
    permission_classes = [permissions.IsAuthenticated]

class CreateFollower(generics.CreateAPIView):
    serializer_class=FollowerSerializer
    queryset= UserProfile.objects.all()

    def create(self, request, *args, **kwargs):
        id=self.kwargs.get("profile_id")
        profile_instance=get_object_or_404(UserProfile, id=id)

        if profile_instance.follower.filter(id=self.request.user.id).exists():
            profile_instance.follower.remove(self.request.user)
            request.user.userprofile.following.remove(profile_instance.user.id)
            return Response({'detail': 'Following removed successfully'}, status=status.HTTP_201_CREATED)
        else:
            profile_instance.follower.add(self.request.user)
            request.user.userprofile.following.add(profile_instance.user.id)
            return Response({'detail': 'Following added successfully'}, status=status.HTTP_201_CREATED)

    




class ReportCreateView(generics.CreateAPIView):
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        stream_id = self.kwargs.get('stream_id')
        stream = get_object_or_404(Stream, pk=stream_id)

        request.data['reporter'] = self.request.user.id
        request.data['video'] = stream_id

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

       
        report_count = Report.objects.filter(video=stream).count()
        if report_count >= 10:
            
            stream.delete()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
class ChatListCreateView(generics.CreateAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]
    def create(self, request, *args, **kwargs):
        stream_id = self.kwargs.get('stream_id')
        stream = get_object_or_404(Stream, pk=stream_id)

        request.data['user'] = self.request.user.id
        request.data['stream'] = stream_id

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
  
class CreateLike(generics.CreateAPIView):
    queryset = Stream.objects.all()
    serializer_class = LikeSerializer

    def create(self, request, *args, **kwargs):
        stream_id = self.kwargs.get("stream_id")
        stream = get_object_or_404(Stream, id=stream_id)

        user = self.request.user
        if stream.liked_by.filter(id=user.id).exists():
            stream.liked_by.remove(user)
            return Response({'detail': 'Like removed successfully'}, status=status.HTTP_200_OK)
        else:
            stream.liked_by.add(user)
            return Response({'detail': 'Like added successfully'}, status=status.HTTP_201_CREATED)
        

class Subscribeview(generics.CreateAPIView):
    queryset = Stream.objects.all()
    serializer_class = LikeSerializer

    def create(self, request, *args, **kwargs):
        id = self.kwargs.get('profile_id')
        profile_instance = get_object_or_404(UserProfile,id=id)
        user = request.user
        if profile_instance.subscriber.filter(id = request.user.id).exists():
            profile_instance.subscriber.remove(user)
            request.user.userprofile.subscribing.remove(profile_instance.user.id)
            return Response({'detail': 'subscriber removed successfully'}, status=status.HTTP_201_CREATED)
        else:
            profile_instance.subscriber.add(user)
            request.user.userprofile.subscribing.add(profile_instance.user.id)
            return Response({'detail':'You are now subscribed to this account!'},status=status.HTTP_201_CREATED)