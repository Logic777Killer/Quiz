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
    path('survey/<int:survey_id>/', views.start_survey, name='start_survey'),
    path('survey/<int:survey_id>/question/<int:question_index>/', views.take_survey, name='take_survey'),
    path('stats/user-passed/', views.stats_user_passed, name='stats_user_passed'),
    path('stats/my-surveys/', views.stats_my_surveys, name='stats_my_surveys'),
    path('stats/all/', views.stats_all_surveys, name='stats_all_surveys'),
    path('stats/my-surveys/<int:survey_id>/', views.stats_my_survey_detail, name='stats_my_survey_detail'),
]
