from devices.views import *
from weather.models import Weather

# Weathers

def weathers(request):
    if request.method == 'POST':
        try:
            weather_name = request.POST['name']
        except KeyError:
            return JsonResponseBadRequest(reason="No name parameter supplied.")
        # if POST add new weather
        try:
            Weather.objects.get(pk=weather_name)
            return JsonResponseBadRequest(reason="Weather with supplied name already exists.")
        except Weather.DoesNotExist:
            description = request.POST.get('description', default=None)
            z = Weather(name=weather_name, description=description)
            z.save()
            rdevices = {'count': 1, 'data': [z.as_json()]}
            return JsonResponseCreated(data=rdevices)
    else:
        # if GET return list of weathers
        zns = Weather.objects.all().order_by('name')
        rweathers = {'count': len(zns), 'data': [z.as_json() for z in zns]}
        return JsonResponse(data=rweathers)


def weather(request, weather_name):
    try:
        z = Weather.objects.get(pk=weather_name)
    except Weather.DoesNotExist:
        return JsonResponseNotFound(reason="No Weather with the specified id was found.")
    if request.method == 'PATCH':
        # if PATCH add data for weather
        # can't change pk (name)
        try:
            z.description = request.POST['description']
            z.save()
        except KeyError:
            pass
        z.save()
        return JsonResponseNoContent()
    elif request.method == 'DELETE':
        # if DELETE delete sensor
        z.delete()
        return JsonResponseNoContent()
    else:
        # if GET get weather meta data
        rweather = {'count': 1, 'data': [z.as_json()]}
        return JsonResponse(data=rweather)


def sensors_for_weather(weather_name):
    # if GET get weather meta data
    try:
        z = Weather.objects.get(pk=weather_name)
    except Weather.DoesNotExist:
        return JsonResponseNotFound(reason="No Weather with the specified id was found.")
    # devices_views for weather
    rsensors = {'count': 3, 'data': [s.as_json for s in (z.sensor_temp, z.sensor_wind, z.sensor_sun)]}
    return JsonResponse(data=rsensors)


# url options for GET
# targettime=<datetime: targettime> get data <= <targettime>, default is now
# datapts=<int: datapts> get <datapts> sensor reading back from target time, default is 1
# default is to get latest sensor reading for sensor
def weather_data(request, weather_name):
    # if GET get weather meta data
    try:
        z = Weather.objects.get(pk=weather_name)
    except Weather.DoesNotExist:
        return JsonResponseNotFound(reason="No Weather with the specified id was found.")
    dseries = {'sensor_temp': get_tempsensor_data(request, z.sensor_temp),
               'sensor_out': get_windsensor_data(request, z.sensor_wind),
               'sensor_sun': get_sunsensor_data(request, z.sensor_sun),
                }
    rsensordata = {'count': 1, 'data': dseries}
    return JsonResponse(data=rsensordata)


