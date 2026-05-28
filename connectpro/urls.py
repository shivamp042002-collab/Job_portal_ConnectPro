from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="ConnectPro API",
        default_version='v1',
        description="Professional Networking Platform API",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/',     include('apps.accounts.urls')),
    path('api/v1/profiles/', include('apps.profiles.urls')),
    path('api/v1/posts/',    include('apps.posts.urls')),
    path('api/v1/messages/', include('apps.messaging.urls')),
    path('accounts/',        include('allauth.urls')),
    path('api/docs/',  schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc',   cache_timeout=0), name='redoc'),
    path('', include('apps.accounts.frontend_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)