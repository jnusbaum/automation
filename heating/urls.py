from django.urls import path

from . import views

urlpatterns = [
    path('heating/', views.dashboard, name='dashboard'),
    path('heating/all/', views.all, name='view_all'),
    path('heating/overlay/', views.overlay, name='view_overlay'),
    path('heating/<zone_name>/', views.zone, name='view_zone'),
]
