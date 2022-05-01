# -*- codding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image

class Message(models.Model):
    sender = models.ForeignKey(User, 
                               related_name="sent_messages",
                               on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, 
                               related_name="received_messages",
                               on_delete=models.CASCADE)
    message = models.TextField()
    seen = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)
    class Meta:
        ordering = ('date_created', )
    def __str__(self):
        return self.message