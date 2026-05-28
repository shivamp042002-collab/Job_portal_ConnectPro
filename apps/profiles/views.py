from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import Profile, Experience, Education, Follow
from .serializers import ProfileSerializer, ExperienceSerializer, EducationSerializer

User = get_user_model()


class MyProfileView(generics.RetrieveUpdateAPIView):
    serializer_class   = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def get_serializer_context(self):
        return {'request': self.request}


class UserProfileView(generics.RetrieveAPIView):
    serializer_class   = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = get_object_or_404(User, username=self.kwargs['username'])
        profile, _ = Profile.objects.get_or_create(user=user)
        return profile

    def get_serializer_context(self):
        return {'request': self.request}


class FollowToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        target = get_object_or_404(User, username=username)
        if target == request.user:
            return Response({'error': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)
        follow, created = Follow.objects.get_or_create(follower=request.user, following=target)
        if not created:
            follow.delete()
            return Response({'message': f'Unfollowed {username}.', 'is_following': False})
        return Response({'message': f'Now following {username}.', 'is_following': True}, status=status.HTTP_201_CREATED)


class FollowersListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        user      = get_object_or_404(User, username=username)
        followers = Follow.objects.filter(following=user).select_related('follower')
        data = [{'username': f.follower.username, 'followed_at': f.created_at} for f in followers]
        return Response({'count': len(data), 'followers': data})


class FollowingListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        user      = get_object_or_404(User, username=username)
        following = Follow.objects.filter(follower=user).select_related('following')
        data = [{'username': f.following.username, 'followed_at': f.created_at} for f in following]
        return Response({'count': len(data), 'following': data})


class ExperienceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        serializer = ExperienceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(profile=profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        exp = get_object_or_404(Experience, pk=pk, profile=profile)
        exp.delete()
        return Response({'message': 'Deleted.'})


class EducationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        serializer = EducationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(profile=profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        edu = get_object_or_404(Education, pk=pk, profile=profile)
        edu.delete()
        return Response({'message': 'Deleted.'})