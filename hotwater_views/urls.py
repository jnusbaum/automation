from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='view_hotwater_dashboard'),
    path('heater/<heater_name>', views.heater, name='view_hotwater_heater'),
    path('pump/<pump_name>', views.pump, name='view_hotwater_pump'),
]
