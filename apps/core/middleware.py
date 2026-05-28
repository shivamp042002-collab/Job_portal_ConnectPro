import logging
import time
import re
from django.http import JsonResponse
from django.conf import settings

logger = logging.getLogger(__name__)


class SecurityHeadersMiddleware:
    """
    Adds security headers to every response.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Prevent clickjacking
        response['X-Frame-Options'] = 'DENY'

        # Prevent MIME sniffing
        response['X-Content-Type-Options'] = 'nosniff'

        # XSS protection
        response['X-XSS-Protection'] = '1; mode=block'

        # Referrer policy
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'

        # Permissions policy — disable unused browser features
        response['Permissions-Policy'] = (
            'geolocation=(), microphone=(), camera=(), '
            'payment=(), usb=(), magnetometer=()'
        )

        # Remove server info
        if 'Server' in response:
            del response['Server']

        return response


class RequestLoggingMiddleware:
    """
    Logs all API requests with timing info.
    Skips static/media files.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip static and media files
        if request.path.startswith(('/static/', '/media/')):
            return self.get_response(request)

        start_time = time.time()
        response   = self.get_response(request)
        duration   = round((time.time() - start_time) * 1000, 2)

        # Log API requests
        if request.path.startswith('/api/'):
            user = (
                request.user.email
                if hasattr(request, 'user') and request.user.is_authenticated
                else 'anonymous'
            )
            logger.info(
                f"{request.method} {request.path} "
                f"| {response.status_code} "
                f"| {duration}ms "
                f"| {user} "
                f"| {request.META.get('REMOTE_ADDR', '')}"
            )

        return response


class InputSanitizationMiddleware:
    """
    Blocks obviously malicious input patterns.
    Checks POST/PUT/PATCH request bodies.
    """
    # Patterns that suggest SQL injection or XSS
    DANGEROUS_PATTERNS = [
        r'<script[^>]*>',
        r'javascript:',
        r'on\w+\s*=',
        r'union\s+select',
        r'drop\s+table',
        r';\s*delete\s+from',
        r'insert\s+into.*values',
        r'exec\s*\(',
        r'xp_cmdshell',
    ]

    def __init__(self, get_response):
        self.get_response = get_response
        self.patterns     = [
            re.compile(p, re.IGNORECASE)
            for p in self.DANGEROUS_PATTERNS
        ]

    def __call__(self, request):
        if request.method in ('POST', 'PUT', 'PATCH'):
            body = request.body.decode('utf-8', errors='ignore')
            for pattern in self.patterns:
                if pattern.search(body):
                    logger.warning(
                        f"Blocked malicious input from "
                        f"{request.META.get('REMOTE_ADDR')} "
                        f"on {request.path}"
                    )
                    return JsonResponse({
                        'error':  'Invalid input detected.',
                        'code':   'invalid_input',
                        'status': 400,
                    }, status=400)
        return self.get_response(request)


class JWTAuthMiddleware:
    """
    Blocks requests to protected API routes
    that have obviously invalid Authorization headers.
    """
    PUBLIC_PATHS = [
        '/api/v1/auth/login/',
        '/api/v1/auth/register/',
        '/api/v1/auth/token/refresh/',
        '/api/docs/',
        '/api/redoc/',
        '/admin/',
        '/accounts/',
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api/') and \
           not any(request.path.startswith(p) for p in self.PUBLIC_PATHS):
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            if auth_header and not auth_header.startswith('Bearer '):
                return JsonResponse({
                    'error':  'Invalid authorization format. Use: Bearer <token>',
                    'code':   'invalid_auth_format',
                    'status': 401,
                }, status=401)
        return self.get_response(request)