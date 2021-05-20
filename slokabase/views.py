from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from rest_framework import status, views
from rest_framework.generics import (CreateAPIView, GenericAPIView,
                                     ListAPIView, ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.response import Response

from .models import Question, Theme, Shloka
from .serializers import (LoginSerializer, QuestionSerializer,
                          ThemeSerializer, ShlokaSerializer,UserSerializers)
from rest_framework.permissions import AllowAny
import json
# class ReferanceLCMView(ListCreateAPIView):
    
#     queryset = Referance.objects.all()
#     serializer_class = ReferanceSerializer

# class ReferanceRUDView(RetrieveUpdateDestroyAPIView):
    
#     queryset = Referance.objects.all()
#     serializer_class = ReferanceSerializer
class ThemeParentView(ListAPIView):
    # queryset = Theme.objects.all()
    serializer_class = ThemeSerializer

    def get_queryset(self):
       
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        if 'pk' in self.kwargs:

            current_theme = Theme.objects.filter(id=self.kwargs['pk'])
            # print(Theme.objects.filter(parent__in=current_theme))
            return Theme.objects.filter(parent__in=current_theme)
        else:
            return Theme.objects.filter(parent=None)

class ThemeQuestionView(ListAPIView):
    # queryset = Theme.objects.all()
    serializer_class = QuestionSerializer

    def get_queryset(self):
       
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        if 'pk' in self.kwargs:

            current_theme = Theme.objects.filter(id=self.kwargs['pk'])
            # print(Theme.objects.filter(parent__in=current_theme))
            return Question.objects.filter(tag__in=current_theme)
        else:
            return Question.objects.filter(tag=None)

class ThemeLCView(ListCreateAPIView):#CreateAPIView, ListAPIView):
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer
    def perform_create(self,serializer):
        raw_data = self.request.data
        if 'parent' not in raw_data:
            try:
                theme = Theme.objects.get(name = raw_data.get('name'))
            except Theme.DoesNotExist:
                theme = Theme(name = raw_data.get('name'))
                theme.save()
        else:
            try:
                try:
                    parent = Theme.objects.get(name=raw_data.get('parent'))
                except Theme.DoesNotExist:
                    parent = Theme(name=raw_data.get('parent'))
                    parent.save()
                theme = Theme.objects.get(name = raw_data.get('name'),parent = parent)
            except Theme.DoesNotExist:
                theme = Theme(name = raw_data.get('name'),parent = parent)
                theme.save()
        return theme
    

class ThemeRUDView(RetrieveUpdateDestroyAPIView):#CreateAPIView, ListAPIView):
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer
    

class ShlokaLCView(ListCreateAPIView):#CreateAPIView, ListAPIView):
    queryset = Shloka.objects.all()
    serializer_class = ShlokaSerializer

class ShlokaRUDView(RetrieveUpdateDestroyAPIView):#CreateAPIView, ListAPIView):
    queryset = Shloka.objects.all()
    serializer_class = ShlokaSerializer
 
class QuestionLCView(ListCreateAPIView):#CreateAPIView, ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    def perform_create(self,serializer):
        print("inside perform create")
        raw_data = self.request.data
        if 'shloka' not in raw_data:
            raise Exception("Shloka doesn't exist")
        else:
            try:
                try:
                    
                    shloka = Shloka.objects.get(referance_text = raw_data.get('shloka'))
                    print(shloka)
                except Shloka.DoesNotExist:
                    raise Exception("Shloka doesn't exist")
                question = Question.objects.get(question_text = raw_data.get('question_text'),shloka = shloka)
            except Question.DoesNotExist:
                question = Question(shloka = shloka,question_text = raw_data.get('question_text'),
                answer_text = raw_data.get('answer_text'))
                question.save()
                for thm in raw_data.getlist('tag'):
                    try:
                        theme = Theme.objects.get(name = thm)
                    except Theme.DoesNotExist:
                        pass
                    question.tag.add(theme)
        return question

class QuestionRUDView(RetrieveUpdateDestroyAPIView):#CreateAPIView, ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    
class UserLView(ListAPIView):
    
    '''
    CreateModel view not working here since it is dependant on question set in serializer
    need to use ReferanceSerializer which doesn't have any dependancy
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializers
    
class UserCMView(CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializers

class UserRUDView(RetrieveUpdateDestroyAPIView):
    
    queryset = User.objects.all()
    serializer_class = UserSerializers


class LoginView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer



# raw_tag = subtag.get('category')
# tag,c = Tag.objects.get_or_create(text=raw_tag.get('text'))
# subtag,c = SubTag.objects.get_or_create(text = subtag.get('text'),category = tag)
# return subtag  
   