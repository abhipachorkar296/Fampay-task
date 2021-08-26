from django.urls import path
from task import views

app_name = "task"
urlpatterns = [
    path('get_videos', views.GetVideos.as_view(), name="get_videos"),
]