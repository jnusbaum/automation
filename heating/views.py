from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.core import serializers
from django.shortcuts import get_object_or_404
from heating.models import Sensor, SensorData

# Create your views here.
def api_index(request):
    # return doc page
    return HttpResponse("Welcome to the home automation API")


def api_sensors(request):
    if request.method == 'POST':
        # if POST add new sensor
        pk = None
        try:
            pk = request.POST['name']
        except KeyError:
            return HttpResponse()

        s = Sensor(name=pk,
                   type=request.POST.get('type', 'TEMP'),
                   address=request.POST.get('address', ''),
                   description=request.POST.get('description', 'temperature sensor'))
        s.save()
        return HttpResponse(status=201)
    else:
        # if GET return list of sensors
        sensors = Sensor.objects.all()
        data = serializers.serialize('json', sensors)
        return JsonResponse(data, safe=False)


def api_sensor(request, sensor_name):
    if request.method == 'PATCH':
        # if PATCH add data for sensor
        sensor = get_object_or_404(Sensor, pk=sensor_name)
        # can't change pk (name)
        try:
            sensor.type = request.POST['type']
        except KeyError:
            pass
        try:
            sensor.address = request.POST['address']
        except KeyError:
            pass
        try:
            sensor.description = request.POST['description']
        except KeyError:
            pass
        sensor.save()
        return HttpResponse(status=204)
    elif request.method == 'DELETE':
        # if DELETE delete sensor
        sensor = get_object_or_404(Sensor, pk=sensor_name)
        sensor.delete()
        return HttpResponse(status=204)
    else:
        # if GET get sensor meta data
        sensor = get_object_or_404(Sensor, pk=sensor_name)
        data = serializers.serialize('json', (sensor, ))
        return JsonResponse(data, safe=False)


bool_values = {
    'on': True,
    'true': True,
    '1': True,
    'True': True,
    'off': False,
    'false': False,
    '0': False,
    'False': False
}


def api_sensor_data(request, sensor_name):
    if request.method == 'POST':
        print("in api_sensor_data")
        # if POST add data for sensor
        timestamp = request.POST.get('timestamp', timezone.now())
        value_real = request.POST.get('value-real')
        if value_real:
            value_real = float(value_real)
            print(value_real)
        value_bool = request.POST.get('value-bool')
        if value_bool:
            value_bool = bool_values[value_bool]
        s = Sensor.objects.get(name=sensor_name)
        sd = SensorData(sensor=s, timestamp=timestamp, value_real=value_real, value_bool=value_bool)
        sd.save()
        return HttpResponse(status=201)
    else:
        # if GET get data for sensor
        s = Sensor.objects.get(name=sensor_name)
        sensordata = s.sensordata_set.all()
        data = serializers.serialize('json', sensordata)
        return JsonResponse(data, safe=False)
