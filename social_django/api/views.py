from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .serializer import LoginSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from api.models import User, Follower
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# Create your views here.


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        if request.method == "POST":
            # user = request.data.get('user', {})
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

@login_required
def follow(request, pk):
    user = get_object_or_404(User, pk = pk)
    already_followed = Follower.objects.filter(user= user, is_followed_by = request.user).first()
    if not already_followed:
        new_follower = Follower(user=user, is_followed_by = request.user)
        new_follower.save()
        follower_count = Follower.objects.filter(user=user).count()
        return JsonResponse({'status':'Following', 'count':follower_count})
    else:
        already_followed.delete()
        follower_count = Follower.objects.filter(user=user).count()
        return JsonResponse({'status':'Not following', 'count':follower_count})
        