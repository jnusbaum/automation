from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='view_heating_dashboard'),
    path('all/', views.all_zones, name='view_heating_all'),
    path('overlay/', views.overlay, name='view_heating_overlay'),
    path('test/<zone_name>/', views.test, name='view_heating_test'),
    path('<zone_name>/', views.zone, name='view_heating_zone'),
]
