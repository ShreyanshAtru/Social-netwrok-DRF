from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import datetime, timedelta
import jwt

# Create your models here.


class User(AbstractUser):
    email = models.EmailField(max_length=30, unique=True)
    username = models.CharField(max_length=10)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': dt.utcfromtimestamp(dt.timestamp())
        }, settings.SECRET_KEY, algorithm='HS256')

        return token


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def get_user_id(self):
        return self.user.pk

    def get_username(self):
        return self.user.username

    def get_followers_count(self):
        return Follower.objects.filter(user = self.user).exclude(is_followed_by = self.user).count()

    def get_following_count(self):
        return Follower.objects.filter(is_followed_by = self.user).count()


class Follower(models.Model): #rename model to UserFollows or find a better name
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    is_followed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='is_followed_by')


    def get_following(self, user):
        return Follower.objects.filter(is_followed_by=user)

    def get_followers(self, user):
        return Follower.objects.filter(user=user).exclude(is_followed_by=user)

    def get_following_count(self, user):
        return Follower.objects.filter(is_followed_by=user).count()

    def get_followers_count(self, user):
        return Follower.objects.filter(user=user).count()
        
    def __str__(self):
        return str(self.user.username)


class Post(models.Model):
    """
    Post model, where a title and Description is used to post and 
    the pub_time for created time.

    """
    title = models.CharField(max_length=40)
    description = models.TextField()
    pub_time = models.DateTimeField('Created Date', auto_now=True)

    def get_likes_count(self):
        return PostRate.objects.filter(liked=True, rated_post=self).count()

    def get_dislikes_count(self):
        return PostRate.objects.filter(liked=False, rated_post=self).count()

    
class PostRate(models.Model):
    """
    Like and dislike of a Post 
    """
    liked = models.BooleanField(null=True)
    rated_post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.rated_post

        


