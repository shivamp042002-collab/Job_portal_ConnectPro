from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Returns consistent JSON error responses for ALL errors.
    Format: { "error": "message", "code": "error_code", "details": {} }
    """
    response = exception_handler(exc, context)

    if response is not None:
        error_data = {
            'error':   _get_error_message(response.data),
            'code':    _get_error_code(response.status_code),
            'status':  response.status_code,
            'details': response.data if isinstance(response.data, dict) else {},
        }
        response.data = error_data
        return response

    # Unhandled exceptions — log them + return 500
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return Response({
        'error':  'An unexpected error occurred. Please try again.',
        'code':   'server_error',
        'status': 500,
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def _get_error_message(data):
    if isinstance(data, dict):
        for key in ['detail', 'error', 'message', 'non_field_errors']:
            if key in data:
                val = data[key]
                if isinstance(val, list):
                    return str(val[0])
                return str(val)
        # First field error
        for key, val in data.items():
            if isinstance(val, list) and val:
                return f"{key}: {val[0]}"
            return f"{key}: {val}"
    if isinstance(data, list) and data:
        return str(data[0])
    return str(data)


def _get_error_code(status_code):
    codes = {
        400: 'bad_request',
        401: 'unauthorized',
        403: 'forbidden',
        404: 'not_found',
        405: 'method_not_allowed',
        408: 'request_timeout',
        409: 'conflict',
        429: 'rate_limit_exceeded',
        500: 'server_error',
        503: 'service_unavailable',
    }
    return codes.get(status_code, 'error')