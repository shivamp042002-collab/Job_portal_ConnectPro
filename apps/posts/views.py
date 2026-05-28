from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Post, Like, Comment
from .serializers import PostSerializer, PostCreateSerializer, CommentSerializer
from apps.profiles.models import Follow

User = get_user_model()


class FeedView(generics.ListAPIView):
    """
    Returns posts from users the logged-in user follows
    plus their own posts — paginated, newest first.
    """
    serializer_class   = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Get IDs of people this user follows
        following_ids = Follow.objects.filter(
            follower=user
        ).values_list('following_id', flat=True)

        # Include own posts + followed users' posts
        ids = list(following_ids) + [user.id]
        return Post.objects.filter(
            author_id__in=ids
        ).select_related('author').prefetch_related('likes', 'comments')

    def get_serializer_context(self):
        return {'request': self.request}


from apps.accounts.throttles import PostRateThrottle

class PostCreateView(generics.CreateAPIView):
    serializer_class   = PostCreateSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes   = [PostRateThrottle] 

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # Return full post data after creation
        full = PostSerializer(serializer.instance, context={'request': request})
        return Response(full.data, status=status.HTTP_201_CREATED)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get, update or delete a single post."""
    serializer_class   = PostSerializer
    permission_classes = [IsAuthenticated]
    queryset           = Post.objects.all()

    def get_serializer_context(self):
        return {'request': self.request}

    def update(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return Response(
                {'error': 'You can only edit your own posts.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return Response(
                {'error': 'You can only delete your own posts.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)


class LikeToggleView(APIView):
    """Like or unlike a post."""
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(
            user=request.user,
            post=post
        )
        if not created:
            like.delete()
            return Response({
                'message':    'Post unliked.',
                'is_liked':   False,
                'likes_count': post.likes.count()
            }, status=status.HTTP_200_OK)

        return Response({
            'message':    'Post liked.',
            'is_liked':   True,
            'likes_count': post.likes.count()
        }, status=status.HTTP_201_CREATED)


class CommentListCreateView(generics.ListCreateAPIView):
    """List or create comments on a post."""
    serializer_class   = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(
            post_id=self.kwargs['pk']
        ).select_related('author')

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        serializer.save(author=self.request.user, post=post)


class CommentDeleteView(generics.DestroyAPIView):
    """Delete a comment — only the comment author can delete."""
    serializer_class   = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != request.user:
            return Response(
                {'error': 'You can only delete your own comments.'},
                status=status.HTTP_403_FORBIDDEN
            )
        comment.delete()
        return Response(
            {'message': 'Comment deleted.'},
            status=status.HTTP_200_OK
        )


class UserPostsView(generics.ListAPIView):
    """Get all posts by a specific user."""
    serializer_class   = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        username = self.kwargs['username']
        user     = get_object_or_404(User, username=username)
        return Post.objects.filter(
            author=user
        ).select_related('author').prefetch_related('likes', 'comments')

    def get_serializer_context(self):
        return {'request': self.request}