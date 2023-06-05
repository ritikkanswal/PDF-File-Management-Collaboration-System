from rest_framework import serializers
from .models import User,PDFFile,SharedFile,Comment

class UserSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = User
        fields = '__all__'

class PDFFileSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = PDFFile
        fields = '__all__'
        

class SharedFileSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = SharedFile
        fields = '__all__'
        

class CommentSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Comment
        fields = '__all__'
        