import hashlib
import hmac
from django.conf import settings


def get_client_ip(request):
    """Get real client IP even behind proxy/load balancer."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '')


def mask_email(email):
    """Mask email for safe display: j***@gmail.com"""
    try:
        local, domain = email.split('@')
        masked = local[0] + '***'
        return f"{masked}@{domain}"
    except Exception:
        return '***'


def generate_secure_token(user_id, secret=None):
    """Generate HMAC token for email verification etc."""
    key     = (secret or settings.SECRET_KEY).encode()
    message = str(user_id).encode()
    return hmac.new(key, message, hashlib.sha256).hexdigest()


def paginate_queryset(queryset, page=1, page_size=10):
    """Simple manual pagination helper."""
    start = (page - 1) * page_size
    end   = start + page_size
    total = queryset.count()
    items = queryset[start:end]
    return {
        'total':       total,
        'page':        page,
        'page_size':   page_size,
        'total_pages': (total + page_size - 1) // page_size,
        'has_next':    end < total,
        'has_prev':    page > 1,
        'results':     items,
    }