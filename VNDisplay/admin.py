from django.contrib import admin
from .models import Post

# admin.site.register(Post) . if you want to register the model with the default admin interface

@admin.register(Post) # if you want to register the model with the custom admin interface
class PostAdmin(admin.ModelAdmin): 
    list_display = ['title', 'slug', 'categories', 'date']
    list_filter = ['title', 'date']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['date']