from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class LoginRateThrottle(AnonRateThrottle):
    """5 login attempts per minute per IP."""
    scope = 'login'


class RegisterRateThrottle(AnonRateThrottle):
    """10 registrations per hour per IP."""
    scope = 'register'


class MessageRateThrottle(UserRateThrottle):
    """60 messages per minute per user."""
    scope = 'message'


class PostRateThrottle(UserRateThrottle):
    """30 posts per hour per user."""
    scope = 'post'