from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from .views import PostViewSet, ThreeLayerComment, CommentListView


router = DefaultRouter()
router.register('posts', PostViewSet)
# router.register(r'posts/(?P<post_id>\d+)/comments', TreeCommentViewSet,
#                 basename='comments')


urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    path('posts/<int:post_id>/comments/<int:comment_id>/children/', ThreeLayerComment.as_view()),
    path('posts/<int:post_id>/comments/', CommentListView.as_view()),
    path('', include(router.urls)),
]
