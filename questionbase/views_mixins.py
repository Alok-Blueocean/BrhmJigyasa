from django.shortcuts import render
from rest_framework import views,status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.mixins import ListModelMixin,CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin
from rest_framework.generics import GenericAPIView,RetrieveUpdateDestroyAPIView,ListCreateAPIView
from .serializers import QuestionSerializer,TagSerializer,SubTagSerializer,ReferanceSerializer,ReferanceViewSerializer,TagViewSerializer
from .models import Question,Tag,SubTag,Referance

class ReferanceLCMixinView(ListModelMixin,CreateModelMixin,GenericAPIView):
    
    '''
    CreateModel view not working here since it is dependant on question set in serializer
    need to use ReferanceSerializer which doesn't have any dependancy
    '''
    queryset = Referance.objects.all()
    serializer_class = ReferanceSerializer
        
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

class ReferanceRUDMixinView(UpdateModelMixin,DestroyModelMixin,RetrieveModelMixin,GenericAPIView):
    
    '''
    CreateModel view not working here since it is dependant on question set in serializer
    need to use ReferanceSerializer which doesn't have any dependancy
    '''
    queryset = Referance.objects.all()
    serializer_class = ReferanceSerializer
        
    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)

    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)

    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)