from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.loginView, name='login'),
    path('signup/', views.signup, name='signup'),
    path('hot/', views.hot, name='hot'),
    path('question/<int:question_id>', views.question, name='question'),
    path('settings/', views.settings, name='settings'),
    path('ask/', views.ask, name='ask'),
    path('tag/<str:tag_name>', views.tag, name='tag'),
    path('logout/', views.logoutView, name='logout'),
    path('question/<int:question_id>', views.question, name='answer')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)