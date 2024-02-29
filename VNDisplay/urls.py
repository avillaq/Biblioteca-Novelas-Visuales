from django.urls import path
from VNDisplay.views import home, directory, novel_detail, android, android_apk, android_kirikiroid2, search

app_name = 'VNDisplay'
urlpatterns = [
    path('', view=home, name='home'),
    path('directorio', view=directory, name='directory'),
    path('search', view=search, name='search'),
    path('android', view=android, name='android'),
    path('android/apk', view=android_apk, name='android_apk'),
    path('android/kirikiroid2', view=android_kirikiroid2, name='android_kirikiroid2'),

    path('novel/<int:year>/<int:month>/<int:day>/<slug:title>/', novel_detail, name='novel_detail'),
]