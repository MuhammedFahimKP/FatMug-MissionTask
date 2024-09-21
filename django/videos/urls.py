from django.urls import path 
from .views import (    

    serve_subtitles,
    video_upload_view,
    video_phrase_list_view,
    video_list_retrive_view
)



urlpatterns = [
    path('',video_list_retrive_view,name='list'),
    path('upload/',video_upload_view, name='video upload'),
    path('<int:pk>/',video_list_retrive_view,name='single-view'),
    path('subtitle/<int:pk>/',serve_subtitles,name='subtitles'),
    path('phrase/<int:pk>/',video_phrase_list_view,name='phrase')
]

