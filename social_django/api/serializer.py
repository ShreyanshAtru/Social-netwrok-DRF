from rest_framework import  serializers
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from api.models import User, Follower
from api.models import Profile, Post, PostRate


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    class MEta:
        model = User

        fieds = ['email','password', 'username', 'token']
        extra_kwargs = {'user': {'required': False}}

    def validate(self, data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid". In the case of logging a
        # user in, this means validating that they've provided an email
        # and password and that this combination matches one of the users in
        # our database.
        email = data.get('email', None)
        password = data.get('password', None)

        # Raise an exception if an
        # email is not provided.
        # if email is None:
        #     raise serializers.ValidationError(
        #         'An email address is required to log in.'
        #     )

        # # Raise an exception if a
        # # password is not provided.
        # if password is None:
        #     raise serializers.ValidationError(
        #         'A password is required to log in.'
        #     )
        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }


class ProfileSerialzier(serializers.Serializer):
    class Meta:
        model = Profile 
        fields = ('username', 'user_id', 'followers_count', 'following_count')

        
class FollowerSerializer(serializers.ModelSerializer):
    user = serializers.DictField(child = serializers.CharField(), source = 'get_user_info', read_only = True)
    is_followed_by = serializers.DictField(child = serializers.CharField(), source = 'get_is_followed_by_info', read_only = True)

    class Meta:
        model = Follower
        fields = ('user', 'is_followed_by')
        read_only_fields = ('user', 'is_followed_by')


class PostSerializer(serializers.Serializer):
    likes_count = serializers.IntegerField(source='get_likes_count', read_only = True)
    dislikes_count = serializers.IntegerField(source='get_dislikes_count', read_only = True)

    class Meta:
        model = Post
        fields = ['id', 'pub_date', 'title', 'description', 'likes_count', 'dislikes_count']
        write_only_fields = ['title', 'discription']


class PostRateSerializer(serializers.Serializer):

    class Meta:
        model = PostRate
        fields = ['liked', 'rated_post']
