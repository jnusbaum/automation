from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<zone_name>', views.zone, name='zone'),
]
