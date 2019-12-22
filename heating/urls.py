from django.urls import path

from . import views

urlpatterns = [
    path('heating/', views.index, name='index'),
    path('heating/<zone_name>/', views.zone, name='zone'),
]
