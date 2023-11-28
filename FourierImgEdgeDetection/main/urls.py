from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('download-image', views.download_image, name='download_image'),
]
