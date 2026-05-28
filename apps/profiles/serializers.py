from rest_framework import serializers
from .models import Profile, Experience, Education, Follow
from django.contrib.auth import get_user_model

User = get_user_model()


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'
        read_only_fields = ['profile']


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'
        read_only_fields = ['profile']


class ProfileSerializer(serializers.ModelSerializer):
    username        = serializers.CharField(source='user.username', read_only=True)
    email           = serializers.EmailField(source='user.email', read_only=True)
    experiences     = ExperienceSerializer(many=True, read_only=True)
    education       = EducationSerializer(many=True, read_only=True)
    skills_list     = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    is_following    = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'id', 'username', 'email', 'bio', 'profile_photo',
            'location', 'website', 'phone', 'headline', 'skills',
            'skills_list', 'followers_count', 'following_count',
            'is_following', 'experiences', 'education', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def get_skills_list(self, obj):
        return obj.get_skills_list()

    def get_followers_count(self, obj):
        return obj.user.followers.count()

    def get_following_count(self, obj):
        return obj.user.following.count()

    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Follow.objects.filter(follower=request.user, following=obj.user).exists()
        return False