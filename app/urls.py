from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('question/<int:question_id>/', views.question_detail, name='question_detail'),
    path('ask/', views.ask_question, name='ask_question'),
]
