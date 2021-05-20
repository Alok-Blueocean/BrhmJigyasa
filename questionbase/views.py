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

from .models import Question, Referance, SubTag, Tag
from .serializers import (LoginSerializer, QuestionGETSerializer,
                          QuestionSerializer, ReferanceSerializer,
                          ReferanceViewSerializer, SubTagSerializer,
                          TagSerializer, TagViewSerializer, UserSerializers)
from rest_framework.permissions import AllowAny

class ReferanceLCMView(ListCreateAPIView):
    
    '''
    CreateModel view not working here since it is dependant on question set in serializer
    need to use ReferanceSerializer which doesn't have any dependancy
    '''
    queryset = Referance.objects.all()
    serializer_class = ReferanceSerializer

class ReferanceRUDView(RetrieveUpdateDestroyAPIView):
    
    queryset = Referance.objects.all()
    serializer_class = ReferanceSerializer
   
class TagLCView(ListCreateAPIView):#CreateAPIView, ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagViewSerializer

class TagRUDView(RetrieveUpdateDestroyAPIView):#CreateAPIView, ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class SubTagLCView(ListCreateAPIView):#CreateAPIView, ListAPIView):
    queryset = SubTag.objects.all()
    serializer_class = SubTagSerializer

    def perform_create(self,serializer):
        tag = get_object_or_404(Tag,pk=self.request.data.get('category').get('tag_id'))
        return serializer.save(category=tag)
        

class SubTagRUDView(RetrieveUpdateDestroyAPIView):#CreateAPIView, ListAPIView):
    queryset = SubTag.objects.all()
    serializer_class = SubTagSerializer
  
class QuestionLCView(ListCreateAPIView):#CreateAPIView, ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return QuestionGETSerializer
        return QuestionGETSerializer 

    def create_subtag(self,subtag):
        raw_tag = subtag.get('category')
        try:
            try:
                tag = Tag.objects.get(text=raw_tag.get('text'))
            except Tag.DoesNotExist:
                tag = Tag(text=raw_tag.get('text'))
                tag.save()
            subtag = SubTag.objects.get(text = subtag.get('text'),category = tag)
        except SubTag.DoesNotExist:
            subtag = SubTag(text = subtag.get('text'),category = tag)
            subtag.save()
        return subtag

    def referance_text_object(self,referance_text):
        try:
            obj = Referance.objects.get(referance_text=referance_text)
        except Referance.DoesNotExist:
            referance_split = referance_text.split()
            if(len(referance_split)==2):
                detail_referance = referance_split[1].split('.')
                if(len(detail_referance)==1):
                    obj = Referance(source=referance_split[0],non_chapter=referance_split[1])
                elif(len(detail_referance)==2):
                    obj = Referance(source=referance_split[0],chapter = int(detail_referance[0]),sloka=int(detail_referance[1]))
                elif(len(detail_referance)==3):
                    obj = Referance(source=referance_split[0],canto = int(detail_referance[0]),chapter = int(detail_referance[1]),sloka=int(detail_referance[2]))
            elif(len(referance_split)==3):
                    detail_referance = referance_split[2].split('.')
                    obj = Referance(source=referance_split[0],non_chapter = int(referance_split[1]),chapter = int(detail_referance[0]),sloka=int(detail_referance[1]))
            obj.save()
        return obj

    def create_referance(self,referance):
        referance_text = referance.get('referance_text')
        referance = self.referance_text_object(referance_text)
        print(referance)
        return referance
    
    def perform_create(self, serializer):
        print(serializer)
        raw_data = self.request.data
        subtag = raw_data.get('subtag')[0]
        referance = raw_data.get('referance')
        referance = self.create_referance(referance)
        subtag = self.create_subtag(subtag)
        print("Before save")
        print(subtag,referance)
        obj = SubTag.objects.filter(subtag_id=subtag.subtag_id)
        serializer.save(subtag = obj,referance = referance)



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
   