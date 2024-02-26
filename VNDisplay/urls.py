from django.urls import path
from VNDisplay.views import home, directory, novel_detail, android

app_name = 'VNDisplay'
urlpatterns = [
    path('', view=home, name='home'),
    path('directorio', view=directory, name='directory'),
    path('android/', view=android, name='android'),
    path('novel/<int:year>/<int:month>/<int:day>/<slug:title>/', novel_detail, name='novel_detail'),



]
