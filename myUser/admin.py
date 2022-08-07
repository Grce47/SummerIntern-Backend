from django.contrib import admin

from .models import Video,pythonCode,LoggedInUser

admin.site.register(Video)      #the models defined are registered in the admin site, so that they can be tweaked there
admin.site.register(pythonCode)
admin.site.register(LoggedInUser)