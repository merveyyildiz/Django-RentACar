from django.urls import path

from . import views
urlpatterns = [
    # hiçbir şey olmadığı zaman views deki index git
    path('', views.index, name='index'),


]