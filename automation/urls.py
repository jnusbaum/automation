"""automation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from automation import views

urlpatterns = [
    path('automation/', views.dashboard, name='view_automation_dashboard'),
    path('automation/plot/', views.plot, name='view_automation_plot'),
    path('automation/admin/', admin.site.urls),
    path('automation/devices/dashboard/', include('devices_views.urls')),
    path('automation/devices/api/', include('devices.urls')),
    path('automation/heating/dashboard/', include('heating_views.urls')),
    path('automation/heating/api/', include('heating.urls')),
    path('automation/hotwater/dashboard/', include('hotwater_views.urls')),
    path('automation/hotwater/api/', include('hotwater.urls')),
    path('automation/weather/dashboard/', include('weather_views.urls')),
    path('automation/weather/api/', include('weather.urls')),
]
