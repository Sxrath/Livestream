from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    links = models.URLField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    following = models.ManyToManyField(User, related_name='following_profiles',blank=True)
    follower = models.ManyToManyField(User, related_name='follower_profiles',blank=True)
    subscribing=models.ManyToManyField(User,related_name='subscribing_profile')
    subscriber=models.ManyToManyField(User,related_name='subscriber_profile')
    def _str_(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    
        
class Stream(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category= models.CharField(max_length=255,default='gaming')
    is_exclusive = models.BooleanField(default=False)
    liked_by = models.ManyToManyField(User,related_name='created_streams')

    #fields for streaming setup
    stream_key = models.CharField(max_length=255, blank=True)
    obs_settings = models.JSONField(default=dict)
    stream_status = models.CharField(max_length=20, default='offline')  
    def __str__(self) -> str:
        return f'{self.title} stream by {self.user}'
   
class Report(models.Model):
    video = models.ForeignKey(Stream, on_delete=models.CASCADE)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    reason = models.TextField()
    def __str__(self) -> str:
        return f'report on {self.video}'
    
class Chat(models.Model):
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f'{self.message} on {self.stream}'
    


    
