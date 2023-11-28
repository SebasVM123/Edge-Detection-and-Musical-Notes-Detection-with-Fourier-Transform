from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('download-image', views.download_image, name='download_image'),
    path('musical-notes', views.musical_notes, name='musical_notes'),
    path('see-sound', views.see_sound, name='see_sound')
]
