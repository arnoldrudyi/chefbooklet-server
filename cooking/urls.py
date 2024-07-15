from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('account.urls')),
    path('dish/', include('dish.urls')),
    path('ingredient/', include('ingredient.urls')),
    path('customer/', include('customer.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
