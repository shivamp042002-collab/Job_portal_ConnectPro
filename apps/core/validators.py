import re
from django.core.exceptions import ValidationError


def validate_username(value):
    """
    Username: 3-30 chars, letters/numbers/underscore only.
    """
    if len(value) < 3:
        raise ValidationError('Username must be at least 3 characters.')
    if len(value) > 30:
        raise ValidationError('Username cannot exceed 30 characters.')
    if not re.match(r'^[a-zA-Z0-9_]+$', value):
        raise ValidationError(
            'Username can only contain letters, numbers and underscores.'
        )
    reserved = ['admin', 'root', 'api', 'static', 'media', 'connectpro']
    if value.lower() in reserved:
        raise ValidationError('This username is reserved.')


def validate_password_strength(value):
    """
    Password must have uppercase, lowercase, digit and be 8+ chars.
    """
    if len(value) < 8:
        raise ValidationError('Password must be at least 8 characters.')
    if not re.search(r'[A-Z]', value):
        raise ValidationError('Password must contain at least one uppercase letter.')
    if not re.search(r'[a-z]', value):
        raise ValidationError('Password must contain at least one lowercase letter.')
    if not re.search(r'\d', value):
        raise ValidationError('Password must contain at least one number.')


def validate_post_content(value):
    """Post content must be 1-3000 chars."""
    if not value or not value.strip():
        raise ValidationError('Post content cannot be empty.')
    if len(value.strip()) > 3000:
        raise ValidationError('Post content cannot exceed 3000 characters.')


def validate_message_content(value):
    """Message content must be 1-1000 chars."""
    if not value or not value.strip():
        raise ValidationError('Message cannot be empty.')
    if len(value.strip()) > 1000:
        raise ValidationError('Message cannot exceed 1000 characters.')


def validate_bio(value):
    """Bio cannot exceed 500 chars."""
    if len(value) > 500:
        raise ValidationError('Bio cannot exceed 500 characters.')


def validate_image_size(image):
    """Profile photos and post images max 5MB."""
    max_size = 5 * 1024 * 1024  # 5MB
    if image.size > max_size:
        raise ValidationError('Image size cannot exceed 5MB.')