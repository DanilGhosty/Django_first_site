
from django.db import models
from django.utils import timezone

# Create your models here.
class Post_category(models.Model):
    category_name = models.CharField(max_length=80)
    category_info = models.CharField(max_length=300)
    category_slug = models.CharField(max_length=50, default="All in")
    class Meta:
        verbose_name_plural = "Categories"
    def __str__(self):
        return f"{self.category_name} URl:{self.category_slug}"

class Post(models.Model):
    title = models.CharField(max_length=40)
    text = models.TextField()
    creation_date = models.DateTimeField(default=timezone.now)
    post_img = models.ImageField(upload_to='blog/static/img',default =None)
    published_date = models.DateTimeField(null=True, blank=True)
    post_slug = models.CharField(max_length=80, default="default_post")
    post_category = models.ForeignKey(Post_category, default=1, on_delete=models.SET_DEFAULT)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title + ' ' + str(self.creation_date)


