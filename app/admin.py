from django.contrib import admin
from .models import User,UserProfile,Stream,Report,Chat
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Stream)
admin.site.register(Report)
admin.site.register(Chat)

