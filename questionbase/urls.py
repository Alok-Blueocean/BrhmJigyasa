from django.contrib import admin
from django.urls import path,include
from .views import UserLView,UserCMView,LoginView,UserRUDView,QuestionRUDView,QuestionLCView,ReferanceLCMView,ReferanceRUDView,TagLCView,TagRUDView,SubTagLCView,SubTagRUDView #ReferanceLCMixinView,ReferanceRUDMixinView#AddQuestionView,TagView,SubTagView,ReferanceView

urlpatterns = [
    # path('questions',AddQuestionView.as_view() ,name='addquestion'),
    path('tags',TagLCView.as_view() ,name='tags'),
    path('tags/<int:pk>/',TagRUDView.as_view() ,name='tags'),
    path('subtags',SubTagLCView.as_view() ,name='subtags'),
    path('subtags/<int:pk>',SubTagRUDView.as_view() ,name='subtags'),
    # path('referances',ReferanceView.as_view() ,name='referances'),
    path('referances',ReferanceLCMView.as_view() ,name='referances'),
    path('referances/<int:pk>',ReferanceRUDView.as_view() ,name='referances'),
    path('questions',QuestionLCView.as_view() ,name='questions'),
    path('questions/<int:pk>',QuestionRUDView.as_view() ,name='questions'),
    path('auth/',include('rest_framework.urls'),name='authentication'),
    path('auth/register/',UserCMView.as_view(),name='user'),
    # path('auth/login/',include('rest_framework.urls'),name='user'),
    path('user/<int:pk>',UserRUDView.as_view(),name='user'),
]