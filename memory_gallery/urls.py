from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.users.urls')),
    path('api/', include('apps.memories.urls')),
        
    # Route all non-API, non-admin requests to your React frontend
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html'), name='index'),
]
