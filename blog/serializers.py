from rest_framework import serializers
from .models import Post, Comment
from account.serializers import UserSerializer
from django.contrib.auth import get_user_model
User = get_user_model()

class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=128)
    slug = serializers.SlugField()
    content = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    published_at = serializers.DateTimeField()
    draft = serializers.BooleanField()
    image = serializers.ImageField()

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.content = validated_data.get('content', instance.content)
        instance.published_at = validated_data.get('published_at', instance.published_at)
        instance.draft = validated_data.get('draft', instance.draft)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance

# class CommnetSerializer(serializers.ModelSerializer):
#     author_detail = UserSerializer(source='author' ,read_only=True)

#     class Meta:
#         model = Comment
#         fields = '__all__'

class CommnetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    content = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    is_confirmed = serializers.BooleanField()

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.content = validated_data.get('content', instance.content)
        instance.is_confirmed = validated_data.get('is_confirmed', instance.is_confirmed)
        instance.save()
        return instance