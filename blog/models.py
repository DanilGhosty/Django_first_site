from django.db import models
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=40)
    text = models.TextField()
    creation_date = models.DateTimeField(default=timezone.now)
    post_img = models.ImageField(upload_to='blog/static/img',default =None)
    published_date = models.DateTimeField(null=True, blank=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title + ' ' + str(self.creation_date)


