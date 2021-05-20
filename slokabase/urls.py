from django.contrib import admin
from django.urls import path,include
from .views import ThemeQuestionView,UserLView,UserCMView,LoginView,UserRUDView,QuestionRUDView,QuestionLCView,ShlokaLCView,ShlokaRUDView,ThemeParentView,ThemeLCView,ThemeRUDView

urlpatterns = [
    # path('questions',AddQuestionView.as_view() ,name='addquestion'),
    
    path('questions',QuestionLCView.as_view() ,name='questions'),
    path('questions/<int:pk>',QuestionRUDView.as_view() ,name='questions'),
     path('shloka',ShlokaLCView.as_view() ,name='shloka'),
    path('shloka/<int:pk>',ShlokaRUDView.as_view() ,name='shloka'),
     path('theme',ThemeLCView.as_view() ,name='theme'),
    path('theme/<int:pk>',ThemeRUDView.as_view() ,name='theme'),
    path('parent/theme',ThemeParentView.as_view() ,name='theme'),
    path('theme/<int:pk>/question',ThemeQuestionView.as_view() ,name='themequestion'),
    path('parent/theme/<int:pk>',ThemeParentView.as_view() ,name='parenttheme'),
    path('auth/',include('rest_framework.urls'),name='authentication'),
    path('auth/register/',UserCMView.as_view(),name='user'),
    # path('auth/login/',include('rest_framework.urls'),name='user'),
    path('user/<int:pk>',UserRUDView.as_view(),name='user'),
]