from rest_framework import serializers
from .models import BlogPost, Category, Tag, Comment, UserProfile
from django.contrib.auth.models import User

from rest_framework import serializers
from .models import BlogPost, Category, Tag, Comment, UserProfile
from django.contrib.auth.models import User

class BlogPostSerializer(serializers.ModelSerializer):
    # Read-only field for the author (so it's not required during creation)
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'created_date', 'published_date', 'author', 'category', 'tags', 'likes']

    def create(self, validated_data):
        # Assign the user who is making the request as the author
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture']
