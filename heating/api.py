from decimal import *
from datetime import datetime
from heating.models import *

from http import HTTPStatus
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, HttpResponseServerError

class HttpResponseNoContent(HttpResponse):
    status_code = HTTPStatus.NO_CONTENT

class HttpResponseCreated(HttpResponse):
    status_code = HTTPStatus.CREATED




def zones(request):
    if request.method == 'POST':
        # if POST add new zone
        z = Zone(name=request.form['name'], description=request.form['description'])
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
        return HttpResponseNoContent()
    elif request.method == 'DELETE':
        # if DELETE delete sensor
        zone.delete()
        return HttpResponseNoContent
    else:
        # if GET get zone meta data
        rzone = {'count': 1, 'data': [zone.as_json()]}
        return JsonResponse(data=rzone)


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
        s = Sensor(name=request.form['name'], type=request.form['type'],
               address=request.form['address'], description=request.form['description'],
               zone=zone)
        s.save()
        return HttpResponseCreated()
    else:
        # if GET return list of sensors
        sensors = Sensor.objects.all().order_by('name')
        rsensors = {'count': len(sensors), 'data': [s.as_json() for s in sensors]}
        return JsonResponse(data=rsensors)


def sensor(request, sensor_name):
    if request.method == 'PATCH':
        # if PATCH add data for sensor
        try:
            sensor = Sensor[sensor_name]
        except ObjectNotFound:
            raise VI404Exception("No Sensor with the specified id was found.")
        # can't change pk (name)
        try:
            sensor.type = request.form['type']
        except KeyError:
            pass
        try:
            sensor.address = request.form['address']
        except KeyError:
            pass
        try:
            sensor.description = request.form['description']
        except KeyError:
            pass
        try:
            zname = request.form['zone']
            try:
                sensor.zone = Zone[zname]
            except ObjectNotFound:
                raise VI404Exception("No Zone with the specified id was found.")
        except KeyError:
            pass
        return "", 204
    elif request.method == 'DELETE':
        # if DELETE delete sensor
        try:
            sensor = Sensor[sensor_name]
        except ObjectNotFound:
            raise VI404Exception("No Sensor with the specified id was found.")
        sensor.delete()
        return "", 204
    else:
        # if GET get sensor meta data
        try:
            sensor = Sensor[sensor_name]
        except ObjectNotFound:
            raise VI404Exception("No Sensor with the specified id was found.")
        rsensor = {'count': 1, 'data': [SensorView.render(sensor)]}
        return jsonify(rsensor)


def sensors_for_zone(request, zone_name):
    # if GET get zone meta data
    try:
        zone = Zone[zone_name]
    except ObjectNotFound:
        raise VI404Exception("No Zone with the specified id was found.")
    # sensors for zone
    rsensors = {'count': len(zone.sensors), 'data': [SensorView.render(s) for s in zone.sensors]}
    return jsonify(rsensors)


# url options for GET
# targettime=<datetime: targettime> get data <= <targettime>, default is now
# datapts=<int: datapts> get <datapts> sensor reading back from target time, default is 1
# default is to get latest sensor reading for sensor
def zone_data(request, zone_name):
    # if GET get zone meta data
    try:
        zone = Zone[zone_name]
    except ObjectNotFound:
        raise VI404Exception("No Zone with the specified id was found.")
    targettime = request.args.get('targettime', default=datetime.today(), type=str_to_datetime)
    datapts = request.args.get('datapts', default=1, type=int)
    dseries = {}
    for sensor in zone.sensors:
        sdata = sensor.data.filter(lambda s: s.timestamp <= targettime).order_by(desc(SensorData.timestamp)).limit(datapts)
        data = []
        bad = 0
        if len(sdata):
            val = sdata[0].value_real
            if val < MIN_TEMP:
                bad += 1
                val = Decimal(MIN_TEMP)
                v = SensorDataView.render(sdata[0], val)
            else:
                v = SensorDataView.render(sdata[0])
            data.append(v)
            for i in range(1, len(sdata)):
                # null all clearly bad values
                prev = val
                val = sdata[i].value_real
                if val < MIN_TEMP or abs(val - prev) > MAX_TEMP_MOVE:
                    bad += 1
                    val = prev
                    v = SensorDataView.render(sdata[i], val)
                else:
                    v = SensorDataView.render(sdata[i])
                data.append(v)
            dseries[sensor.name] = {'count': len(data), 'data': data}
    rsensordata = {'count': 1, 'data': dseries}
    return jsonify(rsensordata)


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
        timestamp = request.form.get('timestamp')
        if timestamp:
            timestamp = str_to_datetime(timestamp)
        else:
            timestamp = datetime.today()
        value_real = request.form.get('value-real')
        if value_real:
            value_real = Decimal(value_real)
        try:
            sensor = Sensor[sensor_name]
        except ObjectNotFound:
            raise VI404Exception("No Sensor with the specified id was found.")
        SensorData(sensor=sensor, timestamp=timestamp, value_real=value_real)
        return "", 201
    else:
        # if GET get data for sensor
        targettime = request.args.get('targettime', default=datetime.today(), type=str_to_datetime)
        datapts = request.args.get('datapts', default=1, type=int)
        try:
            sensor = Sensor[sensor_name]
        except ObjectNotFound:
            raise VI404Exception("No Sensor with the specified id was found.")
        sdata = sensor.data.filter(lambda s: s.timestamp <= targettime).order_by(desc(SensorData.timestamp)).limit(datapts)

        data = []
        bad = 0
        if len(sdata) >= 4:
            # initialize algorithm
            # determine if initial value is bad
            val = sdata[0].value_real
            avgval = mean((val, sdata[1].value_real, sdata[2].value_real, sdata[3].value_real))
            if val < MIN_TEMP or abs(val - avgval) > MAX_TEMP_MOVE:
                # bad value
                bad += 1
                print(f"{sensor.name}: replacing {val} with {avgval} at index 0, timestamp {sdata[0].timestamp}")
                v = SensorDataView.render(sdata[0], val)
            else:
                v = SensorDataView.render(sdata[0])
            data.append(v)
            for i in range(1, len(sdata)):
                # null all clearly bad values
                prev = val
                val = sdata[i].value_real
                if val < MIN_TEMP or abs(val - prev) > MAX_TEMP_MOVE:
                    bad += 1
                    print(f"{sensor.name}: replacing {val} with {prev} at index {i}, timestamp {sdata[i].timestamp}")
                    val = prev
                    v = SensorDataView.render(sdata[i], val)
                else:
                    v = SensorDataView.render(sdata[i])
                data.append(v)
            print(f"{sensor.name}: {bad} bad data points out of {len(sdata)}")
        rsensordata = {'count': len(data), 'data': data}
        return jsonify(rsensordata)

