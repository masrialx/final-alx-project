from rest_framework.routers import DefaultRouter
from .views import BlogPostViewSet, CategoryViewSet, TagViewSet, CommentViewSet,UserProfileViewSet

router = DefaultRouter()
router.register('posts', BlogPostViewSet)
router.register('categories', CategoryViewSet)
router.register('tags', TagViewSet)
router.register('comments', CommentViewSet)
router.register('profiles', UserProfileViewSet)

urlpatterns = router.urls
