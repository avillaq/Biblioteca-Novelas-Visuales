from django.urls import path
from VNDisplay.views import home, directory, completo, allages, yuri, otome, eroge,novel_detail

app_name = 'VNDisplay'
urlpatterns = [
    path('', view=home, name='home'),
    path('directorio', view=directory, name='directory'),
    path('novel/<int:year>/<int:month>/<int:day>/<slug:title>/', novel_detail, name='novel_detail'),
    path('completo/', view=completo, name='completo'),
    path('allages/', view=allages, name='allages'),
    path('yuri/', view=yuri, name='yuri'),
    path('otome/', view=otome, name='otome'),
    path('eroge/', view=eroge, name='eroge'),

]
