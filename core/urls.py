from allauth.account.models import EmailAddress
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from graphene_django.views import GraphQLView
from rest_framework import routers
from rest_framework.authtoken.models import TokenProxy
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf.urls.static import static
from django.conf import settings

from apps.ecommerce.api import ProductViewSet, CategoryViewSet, MainBannerApi, OrderViewSet, sslcommerze_get, \
    SSLGetSessionView, SSLCommerzSuccess, AdvertisementApi, SubscriberViewset, PasswordResetView, SetNewPasswordView
from decouple import config

from apps.ecommerce.report import OrderCount
from apps.ecommerce.schema import schema
from apps.ecommerce.serializers import SetNewPasswordSerializer

admin.site.site_header = 'Red Swiss'
admin.site.site_title = 'Red Swiss'
admin.site.index_title = 'Red Swiss'
admin.site.unregister(TokenProxy)
admin.site.unregister(EmailAddress)


BASE_API_URL = "api/v1/"

router = routers.DefaultRouter()
router.register(r'product', ProductViewSet, basename="product")
router.register(r'category', CategoryViewSet, basename="category")
router.register(r'mainbanner', MainBannerApi, basename="mainbanner")
router.register(r'advertisement', AdvertisementApi, basename="advertisement")
router.register(r'order', OrderViewSet, basename="order")
router.register(r'subscribers', SubscriberViewset, basename="subscribers")

urlpatterns = [
    path(BASE_API_URL, include(router.urls)),
    path(BASE_API_URL+"graphql", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
    path(BASE_API_URL+"docs/", SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path(BASE_API_URL+"auth/password/reset/", PasswordResetView.as_view(), name='rest_password_reset'),
    path(BASE_API_URL+"auth/password/reset/confirm/", SetNewPasswordView.as_view(), name='rest_password_set'),
    path(BASE_API_URL+"auth/", include('dj_rest_auth.urls')),
    path(BASE_API_URL+"auth/registration/", include('dj_rest_auth.registration.urls')),
    path(BASE_API_URL+"payment/sslcommerz/", SSLGetSessionView.as_view(), name="sslcommerze-get"),
    path(BASE_API_URL+"payment/sslcommerz/success/", SSLCommerzSuccess.as_view(), name="sslcommerze-success"),
    path(BASE_API_URL+"reports/sales/", OrderCount.as_view(), name="sales-report"),

    # path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if config('DJANGO_SETTINGS_MODULE') == 'core.settings':
    urlpatterns += [path('admin/', admin.site.urls),]

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin, messages
from django.contrib.auth import views as auth_views
from django.http import HttpResponseRedirect
from django.urls import include, path, re_path, reverse
from django.views.generic import RedirectView
from django.views.static import serve


def make_messages(request):
    messages.add_message(request, messages.INFO, "Info message")
    messages.add_message(request, messages.ERROR, "Error message")
    messages.add_message(request, messages.WARNING, "Warning message")
    messages.add_message(request, messages.SUCCESS, "Success message")

    return HttpResponseRedirect(reverse("admin:index"))


urlpatterns += [
    path("", RedirectView.as_view(pattern_name="admin:index", permanent=False)),
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("make_messages/", make_messages, name="make_messages"),
    path("i18n/", include("django.conf.urls.i18n")),
]

urlpatterns += i18n_patterns(
    path("admin/password_reset/", auth_views.PasswordResetView.as_view(), name="admin_password_reset"),
    path("admin/password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
)

if settings.DEBUG:
    urlpatterns.append(re_path(r"^static/(?P<path>.*)$", serve, kwargs={"document_root": settings.STATIC_ROOT}))

if "debug_toolbar" in settings.INSTALLED_APPS:
    try:
        import debug_toolbar

        urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))
    except ImportError:
        pass
