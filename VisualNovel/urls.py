from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('VNDisplay.urls', namespace='VNDisplay')),
    path('admin/', admin.site.urls),
]
