from rest_framework import serializers
from django.contrib.auth import authenticate, login, logout
from rest_framework import exceptions
from .models import Question,Theme,Shloka
from django.contrib.auth.models import User 



class ThemeparentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = '__all__'
    
class ThemeSerializer(serializers.ModelSerializer):
    parent = ThemeparentSerializer(read_only=True)
    class Meta:
        model = Theme
        fields = '__all__'
        extra_kwargs = {'parent': {'required': False}}
    # def create(self, validated_data):
       
    #     print(validated_data)
    #     category = validated_data.pop('parent')
    #     print(category)
    #     theme = Theme.objects.create(**category)
    #     subtag = Theme.objects.create(parent=theme,**validated_data)
    #     return subtag
# class ReferanceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Referance
#         fields = '__all__'

class ShlokaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shloka
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    #answer = AnswerSerializer(many=False)
    # tag = ThemeSerializer(many=True,read_only = True)
    # shloka = ShlokaSerializer(read_only = True)
    #referance = ReferanceSerializer(many=False,read_only = True)
    # referance = serializers.StringRelatedField(many=False)
    class Meta:
        model = Question
        fields = '__all__'
        depth = 2
        
  
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