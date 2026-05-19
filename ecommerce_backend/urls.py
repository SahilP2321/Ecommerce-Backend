from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Add this function for root URL
def home(request):
    return HttpResponse(
        "<h1>E-commerce API is Running!</h1>"
        "<p>Available endpoints:</p>"
        "<ul>"
        "<li><a href='/admin/'>Admin Panel</a></li>"
        "<li><a href='/swagger/'>API Documentation (Swagger)</a></li>"
        "<li><a href='/redoc/'>API Documentation (Redoc)</a></li>"
        "<li>/api/accounts/ - Authentication endpoints</li>"
        "<li>/api/products/ - Product endpoints</li>"
        "<li>/api/cart/ - Cart endpoints</li>"
        "<li>/api/orders/ - Order endpoints</li>"
        "<li>/api/payments/ - Payment endpoints</li>"
        "</ul>"
    )

schema_view = get_schema_view(
    openapi.Info(
        title="E-commerce API",
        default_version='v1',
        description="API documentation for e-commerce platform",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', home, name='home'),  # Add this line for root URL
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/products/', include('products.urls')),
    path('api/cart/', include('cart.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/payments/', include('payments.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)