"""neeri_recruitment_portal URL Configuration
"""

from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('user/', include('user.urls')),
    path('document/', include('document.urls')),
    path('template/', include('communication_template.urls')),
    path('admin/', admin.site.urls),
]
