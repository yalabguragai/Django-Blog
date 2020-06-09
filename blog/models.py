from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

#our database will have user,post date posted
class post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author=models.ForeignKey(User, on_delete =models.CASCADE)
#to make the post to be more descriptive we use dunder str method
    def __str__(self):
        return  self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk':self.pk})


