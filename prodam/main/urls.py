from . import views
from django.urls import path
from .views import signup_view, login_view, logout_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.main, name='home'),
    path("signup/", signup_view, name='signup'),
    path("login/", login_view, name='login'),
    path("logout/", logout_view, name='logout'),
    path("base-logged/", views.base_logged, name='base-logged'),
    path("profile/", views.profile_view, name='profile'),
    path("settings/", views.settings_view, name='settings'),
    path('base-logged/admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('base-logged/add-ad/', views.add_advertisement, name='add_advertisement'),
    path('advertisement/<int:ad_id>/', views.advertisement_detail, name='advertisement_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)