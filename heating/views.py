from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from heating.models import Sensor, SensorData

# Create your views here.
def api_index(request):
    # return doc page
    return HttpResponse("index")


def api_sensors(request):
    if request.method == 'POST':
        # if POST add new sensor
        s = Sensor(name=request.POST['name'], type=request.POST['type'], address=request.POST['address'], description=request.POST['description'])
        s.save()
    else:
        # if GET return list of sensors
        sensors = Sensor.objects.all()
    return HttpResponse("sensors")


def api_sensor(request, sensor_name):
    if request.method == 'PATCH':
        # if PATCH add data for sensor
        pass
    elif request.method == 'DELETE':
        # if DELETE get data for sensor
        pass
    else:
        # if GET get sensor meta data
        pass
    return HttpResponse("sensor")

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
        print(timestamp)
        value_real = request.POST.get('value-real')
        print(value_real)
        if value_real:
            value_real = float(value_real)
            print(value_real)
        value_bool = request.POST.get('value-bool')
        print(value_bool)
        if value_bool:
            value_bool = bool_values[value_bool]
            print(value_bool)
        s = Sensor.objects.get(name=sensor_name)
        sd = SensorData(sensor=s, timestamp=timestamp, value_real=value_real, value_bool=value_bool)
        sd.save()
    else:
        # if GET get data for sensor
        s = Sensor.objects.get(name=sensor_name)
        data = s.sensordata_set.all()
    return HttpResponse("sensor_data")
