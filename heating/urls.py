from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('all/', views.all_zones, name='view_all'),
    path('overlay/', views.overlay, name='view_overlay'),
    path('test/<zone_name>/', views.test, name='view_test'),
    path('<zone_name>/', views.zone, name='view_zone'),
]
