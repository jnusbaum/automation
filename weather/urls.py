from django.urls import path
from weather import views

urlpatterns = [
    path('weathers/', views.weathers, name='api_weathers'),
    path('weathers/<weather_name>/', views.weather, name='api_weather'),
    path('weathers/<weather_name>/data/', views.weather_data, name='api_weather_data'),
 ]
