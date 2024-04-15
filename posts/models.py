from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager

from users.models import CustomUser



class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Posts.Status.Published)


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name



class Posts(models.Model):

    class Status(models.TextChoices):
        Draft = "DF", "Draft"
        Published = "PB", "Published"

    title = models.CharField(max_length=100)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(upload_to='posts/images/')
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE
                                 )
    published_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
                                max_length=2,
                                choices=Status.choices,
                                default=Status.Draft,
                              )
    recommended = models.BooleanField(default=False)
    tags = TaggableManager()

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title

    @property
    def get_hit_count(self):
        return HitCount.objects.filter(post=self).count()


class HitCount(models.Model):
    ip_address = models.GenericIPAddressField()
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.ip_address} => {self.post}'




class Contact(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    message = models.TextField()

    def __str__(self):
        return self.email


class Comment(models.Model):
    posts = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')

    body = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_time']

    def __str__(self):
        return f"Comment - {self.body} by {self.user}"
