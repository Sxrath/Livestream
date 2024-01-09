from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from .views import CreateProfile,LoginView, Register,UpdateProfile,StreamListCreateView, StreamDetailView, ReportCreateView, ChatListCreateView,CreateLike,CreateFollower,Subscribeview

urlpatterns = [
    path('register/',Register.as_view(),name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('createprofile/',CreateProfile.as_view(),name='create-profile'),
    path('Updateprofile/<int:pk>/',UpdateProfile.as_view(),name='update-profile'),
    path('streams/', StreamListCreateView.as_view(), name='stream-list-create'),
    path('streams/<int:pk>/', StreamDetailView.as_view(), name='stream-detail'),
    path('report-video/<int:stream_id>/', ReportCreateView.as_view(), name='report-create'),
    path('chats/<int:stream_id>/', ChatListCreateView.as_view(), name='chat-list-create'),
    path('follow-following-remove/<int:profile_id>/',CreateFollower.as_view(),name='following'),
    path('like/create/<int:stream_id>/',CreateLike.as_view(),name='like'),
    path('sub-create-delete/<int:profile_id>/',Subscribeview.as_view(),name='sub')

]


