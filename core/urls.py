from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers
from apps.ecommerce.api import ProductViewSet, CategoryViewSet

BASE_API_URL = "api/v1/"

router = routers.DefaultRouter()

router.register(r'product', ProductViewSet, basename="product")
router.register(r'category', CategoryViewSet, basename="category")

urlpatterns = [
    path('admin/', admin.site.urls),
    path(BASE_API_URL, include(router.urls)),
    path(BASE_API_URL+"docs/", SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path(BASE_API_URL+"auth/", include('dj_rest_auth.urls')),
    path(BASE_API_URL+"auth/registration/", include('dj_rest_auth.registration.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
]

