from django.shortcuts import render
from rest_framework import views,status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.mixins import ListModelMixin,CreateModelMixin
from rest_framework.generics import GenericAPIView
from .serializers import QuestionSerializer,TagSerializer,SubTagSerializer,ReferanceSerializer,ReferanceViewSerializer,TagViewSerializer
from .models import Question,Tag,SubTag,Referance

class AddQuestionView(views.APIView):
    def __init__(self, *args, **kwargs):
        pass
    def get(self,request):
        questions = Question.objects.all()
        question_response = QuestionSerializer(questions,many=True)
        return Response(question_response.data)
    def post(self,request):
        pass

class TagView(views.APIView):
    def __init__(self, *args, **kwargs):
        pass
    def get(self,request):
        tags = Tag.objects.all()
        tag_response = TagViewSerializer(tags,many=True)
        return Response(tag_response.data)
    def post(self,request):
        """
        just serializer.save() won't work here since the serializer is nested
        so we need to create another serializer with same model
        """
        # tag  = Tag(**request.data)
        # tag.save()
        print("post called")
        tag = TagSerializer(data=request.data)
        print(tag.is_valid())
        if tag.is_valid(raise_exception=True):
            print("valid")
            tag.save()
        return Response(tag.data)

    def put(self,request):
        print('put called')
        print(request.method)
        #tag_o = self.get_object(pk)
        # print(tag_o)
        # print('put called')
        request_data = request.data
        pk = request_data['tag_id']
        print(pk)
        # request_data.pop('tag_id')
        # request_data.pop('text')
        tag_o = get_object_or_404(Tag.objects.all(), pk=pk)
        print(tag_o)
        print(request_data)
        tag = TagViewSerializer(data = request_data,instance=tag_o)
        # tag.save()
        print(tag.is_valid())
        if tag.is_valid(raise_exception=True):
            print("valid")
            tag.save()
        return Response(tag.data)
    
class SubTagView(views.APIView):
    def __init__(self, *args, **kwargs):
        pass
    def get(self,request):
        subtags = SubTag.objects.all()
        subtag_response = SubTagSerializer(subtags,many=True)
        return Response(subtag_response.data)
    def post(self,request):
        """
        just serializer.save() won't work here since the serializer is nested
        so we need to create another serializer with same model
        """
        # tag  = Tag(**request.data)
        # tag.save()
        data = request.data
        print(data['category--------------------']['tag_id'])
        category = Tag.objects.get(tag_id=data['category']['tag_id'])
        print(category)

        tag = SubTagSerializer(data=data)
        print(tag.is_valid())
        if tag.is_valid(raise_exception=True):
            print("valid")
            tag.save()
        return Response(tag.data)

class ReferanceView(views.APIView):
    def __init__(self, *args, **kwargs):
        pass
    def get(self,request):
        referances = Referance.objects.all()
        referance_response = ReferanceViewSerializer(referances,many=True)
        return Response(referance_response.data)
    def post(self,request):
        pass

class ReferanceMixinView(ListModelMixin,GenericAPIView):

    query_set = Referance.objects.all()
    serializer_class = ReferanceViewSerializer
        
    def get(self,request):
        referances = Referance.objects.all()
        referance_response = ReferanceViewSerializer(referances,many=True)
        return Response(referance_response.data)
   