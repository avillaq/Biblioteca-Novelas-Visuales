from django.contrib import admin
from .models import Post, Category, Android_Post, Type

@admin.register(Post) # if you want to register the model with the custom admin interface
class PostAdmin(admin.ModelAdmin): 
    list_display = ["title", "categories", "publicaction_date", "update_date"]
    list_filter = ["title", "categories", "publicaction_date", "update_date"]
    search_fields = ["title"]
    ordering = ["publicaction_date", "update_date"]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin): 
    list_display = ["name"]
    search_fields = ["name"]

@admin.register(Android_Post)
class Android_PostAdmin(admin.ModelAdmin):
    list_display = ["title", "type"]
    list_filter = ["type"]
    search_fields = ["title"]
    ordering = ["id"]

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ["name", "resource"]
    search_fields = ["name"]
