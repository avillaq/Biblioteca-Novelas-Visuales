from django.urls import path
from VNDisplay.views import home, completo, allages, yuri, otome, eroge,novel_detail

app_name = 'VNDisplay'
urlpatterns = [
    path('', view=home, name='home'),
    path('novel/<str:year>/<str:month>/<str:title>/', novel_detail, name='novel_detail'),
    path('completo/', view=completo, name='completo'),
    path('allages/', view=allages, name='allages'),
    path('yuri/', view=yuri, name='yuri'),
    path('otome/', view=otome, name='otome'),
    path('eroge/', view=eroge, name='eroge'),

]
