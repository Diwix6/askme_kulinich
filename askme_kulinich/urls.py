"""
URL configuration for askme_kulinich project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from app import views

urlpatterns = [
    path('', include('app.urls')),
    path('admin/', admin.site.urls),
    # path('ask/', views.ask_question, name="ask_question"),
    # path('question/<int:question_id>/', views.question_detail, name='question_detail'),
    path('tag/<str:tag>/', views.tag_view, name='tag_view'),
    path('settings/', views.settings, name="settings"),
    path('profile/edit/', views.edit_profile, name="edit_profile"),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('hot-questions/', views.hot_questions, name='hot_questions'),
    path('logout/', views.logout_views, name='logout'),
    path('question/vote', views.question_vote_handler, name = "question_vote"),
    # path('mark-correct/', views.mark_correct_answer, name='mark_correct_answer'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)