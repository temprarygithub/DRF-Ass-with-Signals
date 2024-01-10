from rest_framework import serializers
from .models import User_Data
from .models import Post

class UserSerializer(serializers.ModelSerializer): 
    class Meta:
        model = User_Data
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Post
        fields = '__all__'
