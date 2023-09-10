from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):

  user=models.ForeignKey(User,on_delete=models.CASCADE)

  umsg=models.TextField()

  cmsg=models.TextField()

  time=models.DateTimeField()
