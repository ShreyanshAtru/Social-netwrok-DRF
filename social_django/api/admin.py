from django.contrib import admin
from api.models import User , Profile, Follower 
# Register your models here.


class FollowAdmin(admin.ModelAdmin):
    list_display = ('get_follow')

    def get_follow(self, instance):
        return instance.get_followers

admin.site.register(Profile)
admin.site.register(User)
admin.site.register(Follower, FollowAdmin)