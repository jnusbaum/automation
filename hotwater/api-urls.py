from django.urls import path

from . import api

urlpatterns = [
    # zone
    path('waterheaters/', api.waterheaters, name='api_waterheaters'),
    path('waterheaters/<heater_name>/', api.waterheater, name='api_waterheater'),
    path('waterheaters/<heater_name>/data/', api.waterheater_data, name='api_waterheater_data'),

    path('circpumps/', api.circpumps, name='api_circpumps'),
    path('circpumps/<pump_name>/', api.circpump, name='api_circpump'),
    path('circpumps/<pump_name>/data/', api.circpump_data, name='api_circpump_data'),
]
