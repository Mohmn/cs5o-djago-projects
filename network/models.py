from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    following = models.ManyToManyField('User',blank=True,null=True,related_name="followieng")
    followers = models.ManyToManyField('User',blank=True,null=True,related_name="followees")

class Posts(models.Model):
    post = models.TextField()
    uploaded_by = models.ForeignKey('User',on_delete=models.CASCADE,related_name="posts")
    likes = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)

class Preferences(models.Model):
    user = models.ForeignKey("User",on_delete=models.CASCADE,related_name="my_likes")
    post = models.ForeignKey("Posts",on_delete=models.CASCADE,related_name="p_likes")
    
class Messages(models.Model):
    sender    =   models.ForeignKey("User", on_delete=models.CASCADE,related_name="sended_messages")
    reciever  =   models.ForeignKey("User", on_delete=models.CASCADE,related_name="reciever_messages")
    text      =   models.CharField( max_length=1500)
    read      =   models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    def serialize(self):
        return {
            "sender": self.sender.username,
            "text": self.text,
            "timestamp": self.timestamp.strftime("%b %-d %Y, %-I:%M %p"),
            "read": self.read,
        }

class LastMessageSeen(models.Model):
    user1 =   models.ForeignKey("User", on_delete=models.CASCADE,related_name="u1")
    user2 =   models.ForeignKey("User", on_delete=models.CASCADE,related_name="u2")
    last_time_read = models.DateTimeField(null=True,blank=True)

    def time_read(self):
        msg_tm = self.last_time_read or datetime(1990,1,1,1,1,1)
        return msg_tm

