from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.relations import SlugRelatedField
from django.core.files.base import ContentFile
import base64

from posts.models import Comment, Post, Group, Follow, User


class Base64ImageField(serializers.ImageField):
    """ Сериалайзер для декодирования изображений."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class GroupSerializer(serializers.ModelSerializer):
    """ Сериалайзер для модели Group."""
    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class PostSerializer(serializers.ModelSerializer):
    """ Сериалайзер для модели Post."""
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        fields = '__all__'
        read_only_fields = ('author',)
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    """ Сериалайзер для модели Comment."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields =('post',)


class FollowSerializer(serializers.ModelSerializer):
    """ Сериалайзер для модели Follow со встроенной функцией валидации
    невозможности подписаться на самого себя."""
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    following = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(), fields=['user', 'following']
            )
        ]

    def validate_following(self, data):
        if data == self.context.get('request').user:
            raise serializers.ValidationError('Невозможно подписаться на себя')

        return data
