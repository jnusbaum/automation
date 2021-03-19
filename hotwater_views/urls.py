from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='view_hotwater_dashboard'),
    path('test/heater/<heater_name>', views.test_heater, name='view_heater_test'),
    path('test/pump/<pump_name>', views.test_pump, name='view_pump_test'),
    path('test/spinner', views.test_spinner, name='view_spinner_test'),
]
