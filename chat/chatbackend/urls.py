from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import *
from chatbackend.views import UserViewSet, MessageViewSet, DialogViewSet

router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')
router.register(r'message', MessageViewSet, basename='message')
router.register(r'dialog', DialogViewSet, basename='dialog')


urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


