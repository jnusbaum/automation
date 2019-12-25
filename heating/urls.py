from django.urls import path

from . import views

urlpatterns = [
    path('heating/', views.index, name='index'),
    path('heating/all/', views.view_all, name='view_all'),
    path('heating/<zone_name>/', views.zone, name='zone'),
    path('heating/test/', views.test, name='test')
]
