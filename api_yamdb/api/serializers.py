import datetime

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from reviews.models import Review, Comment, User, Category, Genre, Title


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(
        max_length=150,
        validators=[
            UnicodeUsernameValidator(),
        ]
    )

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        username = data['username']
        email = data['email']
        users = User.objects.filter(Q(username=username) | Q(email=email))
        only_username_exists = (
            users.filter(username=username).exclude(email=email).exists()
        )
        only_email_exists = (
            users.filter(email=email).exclude(username=username).exists()
        )
        if only_username_exists:
            raise ValidationError(
                {'email': f'{username} уже зарегистрирован с другой почтой.'}
            )
        if only_email_exists:
            raise ValidationError(
                {'email': 'Данный адрес электронной почты уже используется.'}
            )
        return data

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError(
                {'username': 'Запрещено использовать имя "me".'}
            )
        return value


class RecieveTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        validators=[UnicodeUsernameValidator()],
    )
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=[UnicodeUsernameValidator()],
    )
    email = serializers.EmailField(
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    bio = serializers.CharField(required=False)
    role = serializers.ChoiceField(choices=User.Roles.choices, required=False)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        lookup_field = 'username'
        extra_kwargs = {'url': {'lookup_field': 'username'}}

    def validate_username(self, value):
        if (
            self.context['request'].method == 'POST'
            and User.objects.filter(username=value).exists()
        ):
            raise serializers.ValidationError(
                {'username': 'Данное имя пользователя уже используется.'}
            )
        return value


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    rating = serializers.IntegerField(read_only=True)
    description = serializers.CharField(required=False)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category', 'rating')
        read_only_fields = ('id',)

    def validate_year(self, value):
        year = datetime.date.today().year
        if year < value:
            raise serializers.ValidationError(
                "Год выпуска не может быть больше текущего"
            )
        return value


class TitleReadOnlySerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category', 'rating')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('id', 'pub_date')
        model = Review

    def validate(self, data):
        title_id = self.context['view'].kwargs['title_id']
        if (
            self.context['view'].action == 'create'
            and Review.objects.filter(
                title=title_id,
                author=self.context['request'].user
            ).exists()
        ):
            raise ValidationError({'author': 'Вы уже оставляли отзыв.'})
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('id', 'pub_date')
        model = Comment
