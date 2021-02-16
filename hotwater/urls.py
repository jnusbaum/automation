from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='view_hotwater_dashboard'),
    path('test/<heater_name>', views.test_heater, name='view_hotwater_test')
]
