from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import PostViewSet, ThreeLayerComment, CreateDeleteComment


router = DefaultRouter()
router.register('posts', PostViewSet)
router.register(r'posts/(?P<post_id>\d+)/comments', CreateDeleteComment,
               basename='comments')


urlpatterns = [
    path('posts/<int:post_id>/comments/<int:comment_id>/children/',
         ThreeLayerComment.as_view()),

    # path('posts/<int:post_id>/comments/', CreateDeleteComment.as_view({
    #     'delete': 'destroy',
    #     'post': 'create',
    #     'get': 'list'
    # })),
    path('', include(router.urls)),
]

urlpatterns += [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
