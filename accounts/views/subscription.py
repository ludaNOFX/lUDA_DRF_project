from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

User = get_user_model()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, slug):
    user_to_follow = get_object_or_404(User, slug=slug)
    if request.user == user_to_follow:
        return Response({'error': 'You cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)

    user_to_follow.follow(request.user)
    return Response({'status': 'following'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request, slug):
    user_to_unfollow = get_object_or_404(User, slug=slug)
    if request.user == user_to_unfollow:
        return Response({'error': 'You cannot unfollow yourself'}, status=status.HTTP_400_BAD_REQUEST)

    user_to_unfollow.unfollow(request.user)
    return Response({'status': 'unfollowed'}, status=status.HTTP_200_OK)

