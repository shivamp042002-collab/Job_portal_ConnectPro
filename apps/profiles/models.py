from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Profile(models.Model):
    user          = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio           = models.TextField(blank=True, default='')
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    location      = models.CharField(max_length=100, blank=True, default='')
    website       = models.URLField(blank=True, default='')
    phone         = models.CharField(max_length=20, blank=True, default='')
    headline      = models.CharField(max_length=200, blank=True, default='')
    skills        = models.TextField(blank=True, default='')
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'profiles'

    def __str__(self):
        return f"{self.user.username}'s profile"

    def get_skills_list(self):
        return [s.strip() for s in self.skills.split(',')] if self.skills else []


class Experience(models.Model):
    profile     = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='experiences')
    title       = models.CharField(max_length=200)
    company     = models.CharField(max_length=200)
    location    = models.CharField(max_length=100, blank=True)
    start_date  = models.DateField()
    end_date    = models.DateField(null=True, blank=True)
    is_current  = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'experiences'
        ordering = ['-start_date']


class Education(models.Model):
    profile        = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='education')
    school         = models.CharField(max_length=200)
    degree         = models.CharField(max_length=200)
    field_of_study = models.CharField(max_length=200, blank=True)
    start_year     = models.IntegerField()
    end_year       = models.IntegerField(null=True, blank=True)
    description    = models.TextField(blank=True)

    class Meta:
        db_table = 'education'
        ordering = ['-start_year']


class Follow(models.Model):
    follower   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'follows'
        unique_together = ('follower', 'following')