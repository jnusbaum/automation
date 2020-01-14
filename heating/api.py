from decimal import *
from datetime import datetime
from statistics import mean
from heating.models import *
from http import HTTPStatus
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, HttpResponseServerError, HttpResponseBadRequest

MAX_TEMP_MOVE = 25
MIN_TEMP = 30


class HttpResponseNoContent(HttpResponse):
    status_code = HTTPStatus.NO_CONTENT

class HttpResponseCreated(HttpResponse):
    status_code = HTTPStatus.CREATED


def zones(request):
    if request.method == 'POST':
        # if POST add new zone
        z = Zone(name=request.POST['name'], description=request.POST['description'])
        z.save()
        return HttpResponseCreated()
    else:
        # if GET return list of zones
        zones = Zone.objects.order_by('name')
        rzones = {'count': len(zones), 'data': [z.as_json() for z in zones]}
        return JsonResponse(data=rzones)


def zone(request, zone_name):
    try:
        zone = Zone.objects.get(pk=zone_name)
    except Zone.DoesNotExist:
        return HttpResponseNotFound(reaason="No Zone with the specified id was found.")
    if request.method == 'PATCH':
        # if PATCH add data for zone
        # can't change pk (name)
        try:
            zone.description = request.POST['description']
            zone.save()
        except KeyError:
            pass
        zone.save()
        return HttpResponseNoContent()
    elif request.method == 'DELETE':
        # if DELETE delete sensor
        zone.delete()
        return HttpResponseNoContent
    else:
        # if GET get zone meta data
        rzone = {'count': 1, 'data': [zone.as_json()]}
        return JsonResponse(data=rzone)


def sensors_for_zone(request, zone_name):
    # if GET get zone meta data
    try:
        zone = Zone.objects.get(pk=zone_name)
    except Zone.DoesNotExist:
        return HttpResponseNotFound(reaason="No Zone with the specified id was found.")
    # sensors for zone
    rsensors = {'count': len(zone.sensors), 'data': [s.as_json for s in zone.sensors]}
    return JsonResponse(data=rsensors)


def sensors(request):
    if request.method == 'POST':
        # if POST add new sensor
        zone = None
        try:
            zone_name = request.POST['zone']
            try:
                zone = Zone.objects.get(pk=zone_name)
            except Zone.DoesNotExist:
                return HttpResponseNotFound(reaason="No Zone with the specified id was found.")
        except KeyError:
            pass
        s = Sensor(name=request.POST['name'], type=request.POST['type'],
               address=request.POST['address'], description=request.POST['description'],
               zone=zone)
        s.save()
        return HttpResponseCreated()
    else:
        # if GET return list of sensors
        sensors = Sensor.objects.all().order_by('name')
        rsensors = {'count': len(sensors), 'data': [s.as_json() for s in sensors]}
        return JsonResponse(data=rsensors)


def sensor(request, sensor_name):
    try:
        sensor = Sensor.objects.get(pk=sensor_name)
    except Sensor.DoesNotExist:
        return HttpResponseNotFound(reaason="No Sensor with the specified id was found.")
    if request.method == 'PATCH':
        # if PATCH add data for sensor
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
        try:
            zone_name = request.POST['zone']
            try:
                zone = Zone.objects.get(pk=zone_name)
            except Zone.DoesNotExist:
                return HttpResponseNotFound(reason="No Zone with the specified id was found.")
            sensor.zone = zone
        except KeyError:
            pass
        sensor.save()
        return HttpResponseNoContent()
    elif request.method == 'DELETE':
        # if DELETE delete sensor
        sensor.delete()
        return HttpResponseNoContent()
    else:
        # if GET get sensor meta data
        rsensor = {'count': 1, 'data': [sensor.as_json()]}
        return JsonResponse(data=rsensor)


# url options for GET
# targettime=<datetime: targettime> get data <= <targettime>, default is now
# datapts=<int: datapts> get <datapts> sensor reading back from target time, default is 1
# default is to get latest sensor reading for sensor
def zone_data(request, zone_name):
    # if GET get zone meta data
    try:
        zone = Zone.objects.get(pk=zone_name)
    except Zone.DoesNotExist:
        return HttpResponseNotFound(reaason="No Zone with the specified id was found.")
    try:
        targettime = request.GET['targettime']
        targettime = datetime.fromisoformat(targettime)
    except KeyError:
        targettime = datetime.today()
    try:
        datapts = request.GET['datapts']
    except KeyError:
        datapts = 1
    dseries = {}
    for sensor in zone.sensors:
        sdata = sensor.sensordata_set.filter(timestamp__lte=targettime).order_by('-timestamp')[:datapts]
        data = []
        bad = 0
        if len(sdata):
            val = sdata[0].value
            if val < MIN_TEMP:
                bad += 1
                val = Decimal(MIN_TEMP)
                v = sdata[0].as_json(val)
            else:
                v = sdata[0].as_json()
            data.append(v)
            for i in range(1, len(sdata)):
                # null all clearly bad values
                prev = val
                val = sdata[i].value
                if val < MIN_TEMP or abs(val - prev) > MAX_TEMP_MOVE:
                    bad += 1
                    val = prev
                    v = sdata[i].as_json(val)
                else:
                    v = sdata[i].as_json()
                data.append(v)
            dseries[sensor.name] = {'count': len(data), 'data': data}
    rsensordata = {'count': 1, 'data': dseries}
    return JsonResponse(data=rsensordata)


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


# url options for GET
# targettime=<datetime: targettime> get data <= <targettime>, default is now
# datapts=<int: datapts> get <datapts> sensor reading back from target time, default is 1
# default is to get latest sensor reading for sensor
def sensor_data(request, sensor_name):
    if request.method == 'POST':
        # if POST add data for sensor
        try:
            timestamp = request.POST['timestamp']
            timestamp = datetime.fromisoformat(timestamp)
        except KeyError:
            timestamp = datetime.today()
        try:
            value = request.POST['value']
            value = Decimal(value)
        except KeyError:
            return HttpResponseBadRequest(reason="Missing value parameter")
        try:
            sensor = Sensor.objects.get(pk=sensor_name)
        except Sensor.DoesNotExist:
            return HttpResponseNotFound("No Sensor with the specified id was found.")
        s = SensorData(sensor=sensor, timestamp=timestamp, value=value, original_value=value)
        s.save()
        return HttpResponseCreated()
    else:
        # if GET get data for sensor
        try:
            targettime = request.GET['targettime']
            targettime = datetime.fromisoformat(targettime)
        except KeyError:
            targettime = datetime.today()
        try:
            datapts = request.GET['datapts']
        except KeyError:
            datapts = 1
        try:
            sensor = Sensor.objects.get(pk=sensor_name)
        except Sensor.DoesNotExist:
            return HttpResponseNotFound("No Sensor with the specified id was found.")
        sdata = sensor.sensordata_set.filter(timestamp__lte=targettime).order_by('-timestamp')[:datapts]

        data = []
        bad = 0
        if len(sdata) >= 4:
            # initialize algorithm
            # determine if initial value is bad
            val = sdata[0].value
            avgval = mean((val, sdata[1].value, sdata[2].value, sdata[3].value))
            if val < MIN_TEMP or abs(val - avgval) > MAX_TEMP_MOVE:
                # bad value
                bad += 1
                print(f"{sensor.name}: replacing {val} with {avgval} at index 0, timestamp {sdata[0].timestamp}")
                v = sdata[0].as_json(val)
            else:
                v = sdata[0].as_json()
            data.append(v)
            for i in range(1, len(sdata)):
                # null all clearly bad values
                prev = val
                val = sdata[i].value
                if val < MIN_TEMP or abs(val - prev) > MAX_TEMP_MOVE:
                    bad += 1
                    print(f"{sensor.name}: replacing {val} with {prev} at index {i}, timestamp {sdata[i].timestamp}")
                    val = prev
                    v = sdata[i].as_json(val)
                else:
                    v = sdata[i].as_json()
                data.append(v)
            print(f"{sensor.name}: {bad} bad data points out of {len(sdata)}")
        rsensordata = {'count': len(data), 'data': data}
        return JsonResponse(data=rsensordata)

