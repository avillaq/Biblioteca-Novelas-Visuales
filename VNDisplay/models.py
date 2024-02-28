from django.db import models
from django.urls import reverse
import json
from django.core.serializers.json import DjangoJSONEncoder

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



class PostDetail(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    synopsis = models.TextField()
    image_urls = models.TextField(blank=True)
    details = models.TextField(blank=True)

    def set_image_urls(self, data):
        self.image_urls = json.dumps(data, cls=DjangoJSONEncoder)

    def get_image_urls(self):
        return json.loads(self.image_urls)

    def set_details(self, data):
        self.details = json.dumps(data, cls=DjangoJSONEncoder)

    def get_details(self):
        return json.loads(self.details)

    def __str__(self):
        return self.post.title

class Android_Post(models.Model):
    title = models.CharField(max_length=250)
    full_url = models.URLField(max_length=250)
    image_url = models.URLField(max_length=250)
    type = models.ForeignKey('Type', on_delete=models.CASCADE)

    class Meta:
        db_table = "android_post"

    def __str__(self):
        return self.title

class Type(models.Model):
    name = models.CharField(max_length=250)
    resource = models.URLField(max_length=250, null=True)

    class Meta:
        db_table = "type"

    def __str__(self):
        return self.name
 