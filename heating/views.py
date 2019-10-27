from django.http import HttpResponse
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


def api_sensor_data(request, sensor_name):
    if request.method == 'POST':
        # if POST add data for sensor
        value_real = request.POST.get('value-real')
        value_bool = request.POST.get('value-bool')
        s = Sensor.objects.get(name=sensor_name)
        sd = SensorData(sensor=s, value_real=value_real, value_bool=value_bool)
        sd.save()
    else:
        # if GET get data for sensor
        s = Sensor.objects.get(name=sensor_name)
        data = s.sensordata_set.all()
    return HttpResponse("sensor_data")
