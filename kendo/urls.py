from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.registration_view, name='registration'),
    path('posts/', views.PostViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('posts/<int:pk>/', views.PostViewSet.as_view({'get': 'retrieve'})),
]