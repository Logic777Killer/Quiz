from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('topics/', views.topics_list, name='topics_list'),
    path('topics/<int:topic_id>/', views.topic_surveys, name='topic_surveys'),
    path('create/', views.create_survey, name='create_survey'),
    path('survey/<int:survey_id>/add-questions/', views.add_questions, name='add_questions'),
    path('survey/<int:survey_id>/delete/', views.delete_survey, name='delete_survey'),
]
