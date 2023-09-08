from django.urls import path
from ldubgdbot.api import views

urlpatterns = [
    path('group_list', views.group_list),
    path('teacher_test_message', views.teacher_res)
    ]
