from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("posts/", views.posts_json, name="posts_json"),
    path("posts/<int:pk>/", views.post_detail_json, name="post_detail_json"),
    path("posts/<int:pk>/comments/", views.add_comment, name="add_comment"),
]