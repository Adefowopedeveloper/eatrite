from django.urls import path
from django.conf import settings
from django.conf.urls.static import static  # <-- This import is required
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('cart/', views.cart, name='cart'),
    path('about/', views.about, name='about'),
    path('submit-order/', views.submit_order, name='submit_order'),
]

# Add this only if settings.DEBUG is True (optional but recommended)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
