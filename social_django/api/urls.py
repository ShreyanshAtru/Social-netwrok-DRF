from django.urls import path, include
from .views import LoginAPIView
from .import views


urlpatterns = [
    path('api/login', LoginAPIView.as_view()),
     path('api/follow/<int:pk>/', views.follow, name='follow'),
]