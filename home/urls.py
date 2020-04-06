from django.urls import path

from . import views
#ana urls.py burayı çağırıyor burdanda views.pydeki index fonks çağırıyoruz
urlpatterns = [
    # hiçbir şey olmadığı zaman views deki index git
    path('', views.index, name='index'),
    # ex: /polls/5/
   # path('<int:question_id>/', views.detail, name='detail'),

]