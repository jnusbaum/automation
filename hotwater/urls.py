from django.urls import path

from . import views

urlpatterns = [
    # zone
    path('waterheaters/', views.waterheaters, name='api_waterheaters'),
    path('waterheaters/<heater_name>/', views.waterheater, name='api_waterheater'),
    path('waterheaters/<heater_name>/data/', views.waterheater_data, name='api_waterheater_data'),

    path('circpumps/', views.circpumps, name='api_circpumps'),
    path('circpumps/<pump_name>/', views.circpump, name='api_circpump'),
    path('circpumps/<pump_name>/data/', views.circpump_data, name='api_circpump_data'),
]
