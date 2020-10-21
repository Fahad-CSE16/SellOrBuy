
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from product.pdf import admin_order_pdf

import notifications.urls
from .sitemaps import ProductSitemap,StaticViewSitemap
from django.contrib.sitemaps.views import sitemap
sitemaps={'static':StaticViewSitemap,'products':ProductSitemap}
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('session/', include('Session.urls')),
    path('admin/admin_order_pdf/<int:order_id>/',admin_order_pdf,name='admin_order_pdf'),

    
    path('accounts/login/', admin.site.urls),
    path('', include('product.urls')),
    path('inbox/notifications/',
         include(notifications.urls, namespace='notifications')),
    path('sitemap.xml',sitemap,{'sitemaps':sitemaps},name='django.contrib.sitemaps.views.sitemap'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
