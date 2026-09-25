from django.urls import path

from . import design_views

# {Kendo} ブランチの画面用。main.js は /posts/... を直接呼ぶため、ルート直下に置く。
urlpatterns = [
    path("kendo/", design_views.home, name="home"),
    path("posts/", design_views.posts_json, name="posts_json"),
    path("posts/<int:pk>/", design_views.post_detail_json, name="post_detail_json"),
    path("posts/<int:pk>/comments/", design_views.add_comment, name="add_comment"),
]
