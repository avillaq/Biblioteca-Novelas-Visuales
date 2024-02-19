from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='date')
    full_url = models.URLField(max_length=250)
    image_url = models.URLField(max_length=250)
    description = models.TextField()
    categories = models.CharField(max_length=250)
    date = models.DateField()

    class Meta:
        ordering = ['-date'] #IMPORTANT: Sort by date date in descending order
        db_table = "post"

    def __str__(self):
        return self.title
    
    #IMPORTANT This method will return the canonical URL for a post
    def get_absolute_url(self):
        return reverse('VNDisplay:novel_detail',
                       args=[self.date.year,
                            self.date.month,
                            self.date.day,
                            self.slug])


