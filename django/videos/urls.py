from django.urls import path 
from .views import video_list_view,video_upload_list_view


urlpatterns = [
    path('',video_list_view,name='list'),
    path('upload/',video_upload_list_view, name='video upload'),
    path('jk/<int:pk>/',video_list_view,name='single-view'),
]

