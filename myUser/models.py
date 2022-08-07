from django.db import models
from django.conf import settings
from embed_video.fields import EmbedVideoField
from django.contrib.auth.models import User

class LoggedInUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='logged_in_user',on_delete=models.CASCADE)   #the user whose data is stored
    session_key = models.CharField(max_length=32,blank=True,null=True)  #the 1st session (older)
    session_key_2 = models.CharField(max_length=32,blank=True,null=True)    #the 2nd session (newer)
    def __str__(self):
        return self.user.username


class Video(models.Model):
    title = models.CharField(max_length=100)    #title of the video
    added = models.DateTimeField(auto_now_add=True) #time when it was added
    url = EmbedVideoField(default="https://youtu.be/dQw4w9WgXcQ")   #url of the video

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ['added']


class pythonCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    codearea = models.TextField()
    output = models.TextField()
    session_key = models.TextField(null=True)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    Done = models.BooleanField(default=False)
    Feedback = models.CharField(null=True, default="", max_length=100)

    def __str__(self):
        return str(self.date) + " " + str(self.time)

    class Meta:
        ordering = ['-date','-time']
