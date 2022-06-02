from django.contrib import admin

from .models import Video,pythonCode,LoggedInUser

admin.site.register(Video)
admin.site.register(pythonCode)
admin.site.register(LoggedInUser)