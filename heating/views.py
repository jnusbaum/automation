from django.http import HttpResponse
from heating.models import Sensor, SensorData

# Create your views here.
def api_index(request):
    # return doc page
    return HttpResponse("index")


def api_sensors(request):
    if request.method == 'POST':
        # if POST add new sensor
        s = Sensor(name=request.POST['name'], type=)
        pass
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
        pass
    else:
        # if GET get data for sensor
        pass
    return HttpResponse("sensor_data")
