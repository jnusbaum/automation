from datetime import datetime
from decimal import *
from http import HTTPStatus
from dateutil.parser import *

from django.http import JsonResponse, HttpResponse

from devices.models import *


class JsonResponseNoContent(HttpResponse):
    # this is actually an HttpResponse since JsonResponse has payload by definition
    def __init__(self):
        super().__init__(status=HTTPStatus.NO_CONTENT)


class JsonResponseCreated(JsonResponse):
    def __init__(self, reason="created"):
        super().__init__(status=HTTPStatus.CREATED, data={'error': reason})


class JsonResponseNotFound(JsonResponse):
    def __init__(self, reason="not found"):
        super().__init__(status=HTTPStatus.NOT_FOUND, data={'error': reason})


class JsonResponseServerError(JsonResponse):
    def __init__(self, reason="server error"):
        super().__init__(status=HTTPStatus.INTERNAL_SERVER_ERROR, data={'error': reason})


class JsonResponseBadRequest(JsonResponse):
    def __init__(self, reason="bad request"):
        super().__init__(status=HTTPStatus.BAD_REQUEST, data={'error': reason})


def devices(request):
    if request.method == 'POST':
        try:
            device_name = request.POST['name']
        except KeyError:
            return JsonResponseBadRequest(reason="No name parameter supplied.")
        # if POST add new device
        try:
            Device.objects.get(pk=device_name)
            return JsonResponseBadRequest(reason="Device with supplied name already exists.")
        except Device.DoesNotExist:
            description = request.POST.get('description', default=None)
            z = Device(name=device_name, description=description)
            z.save()
            return JsonResponseCreated()
    else:
        # if GET return list of devices
        zns = Device.objects.all().order_by('name')
        rdevices = {'count': len(zns), 'data': [z.as_json() for z in zns]}
        return JsonResponse(data=rdevices)


def device(request, device_name):
    try:
        z = Device.objects.get(pk=device_name)
    except Device.DoesNotExist:
        return JsonResponseNotFound(reason="No Device with the specified id was found.")
    if request.method == 'PATCH':
        # if PATCH add data for device
        # can't change pk (name)
        try:
            z.description = request.POST['description']
            z.save()
        except KeyError:
            pass
        z.save()
        return JsonResponseNoContent()
    elif request.method == 'DELETE':
        # if DELETE delete device
        z.delete()
        return JsonResponseNoContent()
    else:
        # if GET get device meta data
        rdevice = {'count': 1, 'data': [z.as_json()]}
        return JsonResponse(data=rdevice)


def onewireinterfaces_for_device(device_name):
    # if GET get device meta data
    try:
        z = Device.objects.get(pk=device_name)
    except Device.DoesNotExist:
        return JsonResponseNotFound(reason="No Device with the specified id was found.")
    # devices for device
    rifcs = {'count': len(z.onewireinterface_set), 'data': [s.as_json for s in z.onewireinterfaces]}
    return JsonResponse(data=rifcs)


def tempsensors_for_device(device_name):
    # if GET get device meta data
    try:
        z = Device.objects.get(pk=device_name)
    except Device.DoesNotExist:
        return JsonResponseNotFound(reason="No Device with the specified id was found.")
    # sensors for device
    tsensors = []
    for o in z.onewireinterface_set:
        for s in o.tempsensor_set:
            tsensors.append(s)
    rsensors = {'count': len(tsensors), 'data': [s.as_json for s in tsensors]}
    return JsonResponse(data=rsensors)


def relays_for_device(device_name):
    # if GET get device meta data
    try:
        z = Device.objects.get(pk=device_name)
    except Device.DoesNotExist:
        return JsonResponseNotFound(reason="No Device with the specified id was found.")
    # devices for device
    rifcs = {'count': len(z.relay_set), 'data': [s.as_json for s in z.relay_set]}
    return JsonResponse(data=rifcs)


# one wire interfaces

def onewireinterfaces(request):
    if request.method == 'POST':
        # if POST add new one wire interface
        dev_name = request.POST.get('device', default=None)
        pin_number = request.POST.get('pin', default=None)
        description = request.POST.get('description', default=None)

        s = OneWireInterface(description=description, pin_number=pin_number, device_id=dev_name)
        s.save()
        return JsonResponseCreated()
    else:
        # if GET return list of devices
        ifcs = OneWireInterface.objects.all()
        rifcs = {'count': len(ifcs), 'data': [s.as_json() for s in ifcs]}
        return JsonResponse(data=rifcs)


def onewireinterface(request, ifc_id):
    try:
        s = OneWireInterface.objects.get(pk=ifc_id)
    except OneWireInterface.DoesNotExist:
        return JsonResponseNotFound(reason="No OneWireInterface with the specified id was found.")
    if request.method == 'PATCH':
        # if PATCH add data for onewireinterface
        # can't change pk (name)
        try:
            s.pin_number = request.POST['pin']
        except KeyError:
            pass
        try:
            s.description = request.POST['description']
        except KeyError:
            pass
        try:
            s.device_id = request.POST['device']
        except KeyError:
            pass
        s.save()
        return JsonResponseNoContent()
    elif request.method == 'DELETE':
        # if DELETE delete onewireinterface
        s.delete()
        return JsonResponseNoContent()
    else:
        # if GET get onewireinterface meta data
        rifc = {'count': 1, 'data': [s.as_json()]}
        return JsonResponse(data=rifc)


def get_device_data(request, device: Device):
    sdata = device.devicestatus_set
    try:
        stime = request.GET['starttime']
        stime = isoparse(stime).replace(tzinfo=None)
        sdata = sdata.filter(timestamp__gt=stime)
    except KeyError:
        pass
    try:
        etime = request.GET['endtime']
        etime = isoparse(etime).replace(tzinfo=None)
    except KeyError:
        etime = datetime.utcnow()
    sdata = sdata.filter(timestamp__lte=etime)
    try:
        datapts = request.GET['datapts']
        datapts = int(datapts)
    except KeyError:
        datapts = 1
    sdata = sdata.order_by('-timestamp')[:datapts]
    data = [s.as_json() for s in sdata]
    return {'count': len(data), 'data': data}


# url options for GET
# targettime=<datetime: targettime> get data <= <targettime>, default is now
# datapts=<int: datapts> get <datapts> relay reading back from target time, default is 1
# default is to get latest relay reading for relay
def device_data(request, device_name):
    if request.method == 'POST':
        # if POST add data for relay
        try:
            timestamp = request.POST['timestamp']
            timestamp = datetime.fromisoformat(timestamp)
        except KeyError:
            timestamp = datetime.today()
        try:
            value = request.POST['value']
        except KeyError:
            return JsonResponseBadRequest(reason="Missing value parameter")
        try:
            s = Device.objects.get(pk=device_name)
        except Device.DoesNotExist:
            return JsonResponseNotFound("No Device with the specified id was found.")
        s = DeviceStatus(device=s, timestamp=timestamp, value=value)
        s.save()
        return JsonResponseCreated()
    else:
        # if GET get data for relay
        try:
            s = Device.objects.get(pk=device_name)
        except Device.DoesNotExist:
            return JsonResponseNotFound("No Device with the specified id was found.")
        rdevicedata = get_device_data(request, s)
        return JsonResponse(data=rdevicedata)


# url options for GET
def device_config(request, device_name):
    if request.method == 'GET':
        try:
            d = Device.objects.get(pk=device_name)
        except Device.DoesNotExist:
            return JsonResponseNotFound()

        # one wire temp busses
        djson = {'client_id': d.client_id,
                 'num_interfaces': 0, 'interfaces': [],
                 'num_relays': 0, 'relays': []}
        for onew in d.onewireinterface_set.all():
            ojson = {'pin_number': onew.pin_number, 'tempsensors': [], 'num_tempsensors': 0}
            for s in onew.tempsensor_set.all():
                ojson['tempsensors'].append({'name': s.name, 'address': s.address})
            ojson['num_tempsensors'] = len(ojson['tempsensors'])
            djson['interfaces'].append(ojson)
        djson['num_interfaces'] = len(djson['interfaces'])
        # digital relays
        for rnew in d.relay_set.all():
            djson['relays'].append({'name': rnew.name, 'pin_number': rnew.pin_number})
        djson['num_relays'] = len(djson['relays'])        # not implemented
        return JsonResponse(data=djson)
    else:
        # not implemented
        return JsonResponseBadRequest()


# temperature sensors

def tempsensors(request):
    if request.method == 'POST':
        # if POST add new sensor
        try:
            sensor_name = request.POST['name']
        except KeyError:
            return JsonResponseBadRequest(reason="No name parameter supplied.")
        address = request.POST.get('address', default=None)
        description = request.POST.get('description', default=None)
        try:
            TempSensor.objects.get(pk=sensor_name)
            return JsonResponseBadRequest(reason="TempSensor with supplied name already exists.")
        except TempSensor.DoesNotExist:
            s = TempSensor(name=sensor_name, address=address, description=description)
            s.save()
            return JsonResponseCreated()
    else:
        # if GET return list of devices
        snsrs = TempSensor.objects.all().order_by('name')
        rsensors = {'count': len(snsrs), 'data': [s.as_json() for s in snsrs]}
        return JsonResponse(data=rsensors)


def tempsensor(request, sensor_name):
    try:
        s = TempSensor.objects.get(pk=sensor_name)
    except TempSensor.DoesNotExist:
        return JsonResponseNotFound(reason="No TempSensor with the specified id was found.")
    if request.method == 'PATCH':
        # if PATCH add data for sensor
        # can't change pk (name)
        try:
            s.address = request.POST['address']
        except KeyError:
            pass
        try:
            s.description = request.POST['description']
        except KeyError:
            pass
        s.save()
        return JsonResponseNoContent()
    elif request.method == 'DELETE':
        # if DELETE delete sensor
        s.delete()
        return JsonResponseNoContent()
    else:
        # if GET get sensor meta data
        rsensor = {'count': 1, 'data': [s.as_json()]}
        return JsonResponse(data=rsensor)


def get_tempsensor_data(request, sensor: TempSensor):
    sdata = sensor.tempsensordata_set
    try:
        stime = request.GET['starttime']
        stime = isoparse(stime).replace(tzinfo=None)
        sdata = sdata.filter(timestamp__gt=stime)
    except KeyError:
        pass
    try:
        etime = request.GET['endtime']
        etime = isoparse(etime).replace(tzinfo=None)
    except KeyError:
        etime = datetime.utcnow()
    sdata = sdata.filter(timestamp__lte=etime)
    try:
        datapts = request.GET['datapts']
        datapts = int(datapts)
    except KeyError:
        datapts = 1
    sdata = sdata.order_by('-timestamp')[:datapts]
    data = [s.as_json() for s in sdata]
    return {'count': len(data), 'data': data}


# url options for GET
# targettime=<datetime: targettime> get data <= <targettime>, default is now
# datapts=<int: datapts> get <datapts> sensor reading back from target time, default is 1
# default is to get latest sensor reading for sensor
def tempsensor_data(request, sensor_name):
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
            return JsonResponseBadRequest(reason="Missing value parameter")
        try:
            s = Relay.objects.get(pk=sensor_name)
        except Relay.DoesNotExist:
            return JsonResponseNotFound("No Sensor with the specified id was found.")
        s = TempSensorData(sensor=s, timestamp=timestamp, value=value, original_value=value)
        s.save()
        return JsonResponseCreated()
    else:
        # if GET get data for sensor
        try:
            s = TempSensor.objects.get(pk=sensor_name)
        except TempSensor.DoesNotExist:
            return JsonResponseNotFound("No TempSensor with the specified id was found.")
        rsensordata = get_tempsensor_data(request, s)
        return JsonResponse(data=rsensordata)


# relays

def relays(request):
    if request.method == 'POST':
        # if POST add new relay
        try:
            relay_name = request.POST['name']
        except KeyError:
            return JsonResponseBadRequest(reason="No name parameter supplied.")
        address = request.POST.get('address', default=None)
        description = request.POST.get('description', default=None)
        try:
            Relay.objects.get(pk=relay_name)
            return JsonResponseBadRequest(reason="Relay with supplied name already exists.")
        except Relay.DoesNotExist:
            s = Relay(name=relay_name, address=address, description=description)
            s.save()
            return JsonResponseCreated()
    else:
        # if GET return list of devices
        snsrs = Relay.objects.all().order_by('name')
        rrelays = {'count': len(snsrs), 'data': [s.as_json() for s in snsrs]}
        return JsonResponse(data=rrelays)


def relay(request, relay_name):
    try:
        s = Relay.objects.get(pk=relay_name)
    except Relay.DoesNotExist:
        return JsonResponseNotFound(reason="No Relay with the specified id was found.")
    if request.method == 'PATCH':
        # if PATCH add data for relay
        # can't change pk (name)
        try:
            s.address = request.POST['address']
        except KeyError:
            pass
        try:
            s.description = request.POST['description']
        except KeyError:
            pass
        s.save()
        return JsonResponseNoContent()
    elif request.method == 'DELETE':
        # if DELETE delete relay
        s.delete()
        return JsonResponseNoContent()
    else:
        # if GET get relay meta data
        rrelay = {'count': 1, 'data': [s.as_json()]}
        return JsonResponse(data=rrelay)


def get_relay_data(request, relay: Relay):
    sdata = relay.relaydata_set
    try:
        stime = request.GET['starttime']
        stime = isoparse(stime).replace(tzinfo=None)
        sdata = sdata.filter(timestamp__gt=stime)
    except KeyError:
        pass
    try:
        etime = request.GET['endtime']
        etime = isoparse(etime).replace(tzinfo=None)
    except KeyError:
        etime = datetime.utcnow()
    sdata = sdata.filter(timestamp__lte=etime)
    try:
        datapts = request.GET['datapts']
        datapts = int(datapts)
    except KeyError:
        datapts = 1
    sdata = sdata.order_by('-timestamp')[:datapts]
    data = [s.as_json() for s in sdata]
    return {'count': len(data), 'data': data}


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
# datapts=<int: datapts> get <datapts> relay reading back from target time, default is 1
# default is to get latest relay reading for relay
def relay_data(request, relay_name):
    if request.method == 'POST':
        # if POST add data for relay
        try:
            timestamp = request.POST['timestamp']
            timestamp = datetime.fromisoformat(timestamp)
        except KeyError:
            timestamp = datetime.today()
        try:
            value = request.POST['value']
            value = bool_values[value]
        except KeyError:
            return JsonResponseBadRequest(reason="Missing value parameter")
        try:
            s = Relay.objects.get(pk=relay_name)
        except Relay.DoesNotExist:
            return JsonResponseNotFound("No Sensor with the specified id was found.")
        s = RelayData(relay=s, timestamp=timestamp, value=value)
        s.save()
        return JsonResponseCreated()
    else:
        # if GET get data for relay
        try:
            s = Relay.objects.get(pk=relay_name)
        except Relay.DoesNotExist:
            return JsonResponseNotFound("No Relay with the specified id was found.")
        rrelaydata = get_relay_data(request, s)
        return JsonResponse(data=rrelaydata)
