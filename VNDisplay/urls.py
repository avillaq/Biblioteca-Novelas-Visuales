from django.urls import path
from VNDisplay.views import home, completo, allages, yuri, otome, eroge,novel_detail,delete_all

app_name = 'VNDisplay'
urlpatterns = [
    path('', view=home, name='home'),
    path('novel/<int:year>/<int:month>/<int:day>/<slug:title>/', novel_detail, name='novel_detail'),
    path('delete/', delete_all, name='delete_all'),
    path('completo/', view=completo, name='completo'),
    path('allages/', view=allages, name='allages'),
    path('yuri/', view=yuri, name='yuri'),
    path('otome/', view=otome, name='otome'),
    path('eroge/', view=eroge, name='eroge'),

]
