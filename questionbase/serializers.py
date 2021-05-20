from rest_framework import serializers
from django.contrib.auth import authenticate, login, logout
from rest_framework import exceptions
from .models import Question,Answer,Tag,SubTag,Referance
from django.contrib.auth.models import User 

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
    
class SubTagSerializer(serializers.ModelSerializer):
    """
    required=False if can be created nested objected with one entity
    """
    #category = serializers.StringRelatedField(many=False)
    category = TagSerializer(read_only = True)
    #category_id = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), write_only=True)
    class Meta:
        model = SubTag
        fields = '__all__'
    def not_in_use_create(self,validated_data):
        print("create ..  called")
        print(validated_data)
        category = validated_data.pop('category')
        print(category)
        tag = Tag.objects.create(**category)
        subtag = SubTag.objects.create(category=tag,**validated_data)
        return subtag
    def not_in_use_update(self, instance, validated_data):  
        print("update ..  called")     
        instance.text = validated_data.get('text',instance.text)
        instance.save()


class TagViewSerializer(serializers.ModelSerializer):

    subtag_set = SubTagSerializer(many=True,required = False) 

    class Meta:
        model = Tag
        fields = '__all__'
    # def create(self, validated_data):
    #     print(validated_data)
    #     pass

    def update(self, instance, validated_data,format=None):
        print(validated_data)
        print("update called")
        instance.text = validated_data['text']
        instance.save()

        # Create or update page instances that are in the request
        for item in validated_data['subtag_set']:
            subtag = SubTag(text=item['text'], category = instance)
            subtag.save()
        return instance


class ReferanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referance
        fields = '__all__'

class QuestionGETSerializer(serializers.ModelSerializer):
    #answer = AnswerSerializer(many=False)
    subtag = SubTagSerializer(many=True,read_only = True)
    referance = ReferanceSerializer(many=False,read_only = True)
    # referance = serializers.StringRelatedField(many=False)
    class Meta:
        model = Question
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    #answer = AnswerSerializer(many=False)
    subtag = SubTagSerializer(many=True,read_only = True)
    referance = ReferanceSerializer(many=False,read_only = True)
    # referance = serializers.StringRelatedField(many=False)
    class Meta:
        model = Question
        fields = '__all__'
        
class ReferanceViewSerializer(serializers.ModelSerializer):
    question_set = QuestionSerializer(many=True)
    class Meta:
        model = Referance
        fields = '__all__'
  
  
class UserSerializers(serializers.ModelSerializer): 
    password = serializers.CharField(style={"input_type":"password"},
        max_length=65, min_length=8, write_only=True)
    class Meta: 
        model = User 
        fields =  ['username', 'first_name', 'last_name', 'email', 'password'
                  ]
    def validate(self, attrs):
        email = attrs.get('email', '')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'email': ('Email is already in use')})
        return super().validate(attrs)
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=65, min_length=3, write_only=True)
    username = serializers.CharField(max_length=255, min_length=2)

    class Meta:
        model = User
        fields = ['username', 'password']