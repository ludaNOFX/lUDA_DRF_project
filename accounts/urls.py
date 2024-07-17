# accounts/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views.subscription import follow_user, unfollow_user
from accounts.views.users import UserViewSet

router = DefaultRouter()
router.register(r'', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<slug:slug>/follow/', follow_user, name='follow_user'),
    path('<slug:slug>/unfollow/', unfollow_user, name='unfollow_user'),
]
