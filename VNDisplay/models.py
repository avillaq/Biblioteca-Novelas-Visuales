from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=250)

    class Meta:
        db_table = "category"

    def __str__(self):
        return self.name

class Post(models.Model):

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='date')
    full_url = models.URLField(max_length=250)
    image_url = models.URLField(max_length=250)
    description = models.TextField()
    categories = models.ManyToManyField(Category)
    date = models.DateField()

    class Meta:
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

class Android_Post(models.Model):
    title = models.CharField(max_length=250)
    full_url = models.URLField(max_length=250)
    image_url = models.URLField(max_length=250)

    class Meta:
        db_table = "android_post"

    def __str__(self):
        return self.title
    
 


