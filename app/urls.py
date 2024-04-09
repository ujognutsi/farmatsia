from django.urls import path

from app import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('hot/', views.hot, name='hot'),
    path('questions/<int:question_id>', views.question, name='question')
    # path('', views.index, name='index')
]
