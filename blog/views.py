from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import BlogPost, Category, Tag, Comment, UserProfile
from .serializers import BlogPostSerializer, CategorySerializer, TagSerializer, CommentSerializer, UserProfileSerializer

class BlogPostViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing Blog Posts.
    """
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content', 'tags__name', 'author__username']
    ordering_fields = ['published_date', 'category']

    def perform_create(self, serializer):
        """Automatically assign the currently authenticated user as the author."""
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        """Allow authenticated users to like a post."""
        post = self.get_object()

        # Check if the user has already liked the post
        if request.user in post.likes.all():
            return Response({'status': 'post already liked'}, status=400)  # Return a 400 Bad Request

        # Add the user to the likes if not already liked
        post.likes.add(request.user)
        return Response({'status': 'post liked'})

class CategoryViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing Categories.
    Allows users to create, retrieve, update, and delete categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class TagViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing Tags.
    Allows users to create, retrieve, update, and delete tags.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CommentViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing Comments.
    Allows users to create, retrieve, update, and delete comments.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class UserProfileViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing User Profiles.
    Allows users to create, retrieve, update, and delete their profiles.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Limit the profiles to the authenticated user's profile.
        """
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Automatically assign the currently authenticated user to the profile.
        """
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """
        Allow the user to update their own profile.
        """
        serializer.save()
