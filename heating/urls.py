from django.urls import path

from . import views

urlpatterns = [
    path('heating/', views.dashboard, name='dashboard'),
    path('heating/all/', views.all_zones, name='view_all'),
    path('heating/overlay/', views.overlay, name='view_overlay'),
    path('heating/test/<zone_name>/', views.test, name='view_test'),
    path('heating/<zone_name>/', views.zone, name='view_zone'),
]
