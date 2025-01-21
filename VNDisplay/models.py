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

    id_post = models.CharField(max_length=250, unique=True, blank=True)
    title = models.CharField(max_length=250)
    full_url = models.URLField(max_length=250)
    synopsis = models.TextField()
    cover_url = models.URLField(max_length=300)
    screenshot_urls = models.TextField(blank=True)
    specifications = models.TextField(blank=True)
    categories = models.ManyToManyField(Category)
    publication_date = models.DateField()
    update_date = models.DateField()

    class Meta:
        db_table = "post"

    def set_screenshot_urls(self, data):
        self.screenshot_urls = json.dumps(data, cls=DjangoJSONEncoder)
    
    def get_screenshot_urls(self):
        return json.loads(self.screenshot_urls)
    
    def set_specifications(self, data):
        self.specifications = json.dumps(data, cls=DjangoJSONEncoder)
    
    def get_specifications(self):
        return json.loads(self.specifications)

    def __str__(self):
        return self.title
    
    #IMPORTANT This method will return the canonical URL for a post
    def get_absolute_url(self):
        return reverse('VNDisplay:novel_detail',
                       args=[self.id_post])

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
 