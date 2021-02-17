from hotwater.models import *
from devices.api import *


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


# WaterHeaters

def waterheaters(request):
    if request.method == 'POST':
        try:
            heater_name = request.POST['name']
        except KeyError:
            return JsonResponseBadRequest(reason="No name parameter supplied.")
        # if POST add new waterheater
        try:
            WaterHeater.objects.get(pk=heater_name)
            return JsonResponseBadRequest(reason="WaterHeater with supplied name already exists.")
        except WaterHeater.DoesNotExist:
            description = request.POST.get('description', default=None)
            sensor_in = request.POST.get('sensor_in', default=None)
            sensor_out = request.POST.get('sensor_out', default=None)
            sensor_burn = request.POST.get('sensor_burn', default=None)
            z = WaterHeater(name=heater_name, description=description,
                            sensor_in_id=sensor_in,
                            sensor_out_id=sensor_out,
                            sensor_burn_id=sensor_burn)
            z.save()
            return JsonResponseCreated()
    else:
        # if GET return list of waterheaters
        zns = WaterHeater.objects.all().order_by('name')
        rwaterheaters = {'count': len(zns), 'data': [z.as_json() for z in zns]}
        return JsonResponse(data=rwaterheaters)


def waterheater(request, heater_name):
    try:
        z = WaterHeater.objects.get(pk=heater_name)
    except WaterHeater.DoesNotExist:
        return JsonResponseNotFound(reason="No WaterHeater with the specified id was found.")
    if request.method == 'PATCH':
        # if PATCH add data for waterheater
        # can't change pk (name)
        try:
            z.description = request.POST.get('description', default=z.description)
            z.sensor_in_id = request.POST.get('sensor_in', default=z.sensor_in_id)
            z.sensor_out_id = request.POST.get('sensor_out', default=z.sensor_out_id)
            z.sensor_burn_id = request.POST.get('sensor_burn', default=z.sensor_burn_id)
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
        # if GET get waterheater meta data
        rwaterheater = {'count': 1, 'data': [z.as_json()]}
        return JsonResponse(data=rwaterheater)


# url options for GET
# targettime=<datetime: targettime> get data <= <targettime>, default is now
# datapts=<int: datapts> get <datapts> sensor reading back from target time, default is 1
# default is to get latest sensor reading for sensor
def waterheater_data(request, heater_name):
    # if GET get waterheater meta data
    try:
        z = WaterHeater.objects.get(pk=heater_name)
    except WaterHeater.DoesNotExist:
        return JsonResponseNotFound(reason="No WaterHeater with the specified id was found.")
    dseries = {'sensor_in': get_tempsensor_data(request, z.sensor_in),
               'sensor_out': get_tempsensor_data(request, z.sensor_out),
               'sensor_burn': get_tempsensor_data(request, z.sensor_burn)}
    rsensordata = {'count': 1, 'data': dseries}
    return JsonResponse(data=rsensordata)


# CircPumps

def circpumps(request):
    if request.method == 'POST':
        try:
            pump_name = request.POST['name']
        except KeyError:
            return JsonResponseBadRequest(reason="No name parameter supplied.")
        # if POST add new circpump
        try:
            CircPump.objects.get(pk=pump_name)
            return JsonResponseBadRequest(reason="CircPump with supplied name already exists.")
        except CircPump.DoesNotExist:
            description = request.POST.get('description', default=None)
            sensor = request.POST.get('sensor', default=None)
            relay = request.POST.get('relay', default=None)
            z = CircPump(name=pump_name, description=description,
                         sensor_id=sensor,
                         relay_id=relay)
            z.save()
            return JsonResponseCreated()
    else:
        # if GET return list of circpumps
        pumps = CircPump.objects.all().order_by('name')
        rcircpumps = {'count': len(pumps), 'data': [z.as_json() for z in pumps]}
        return JsonResponse(data=rcircpumps)


def circpump(request, pump_name):
    try:
        z = CircPump.objects.get(pk=pump_name)
    except CircPump.DoesNotExist:
        return JsonResponseNotFound(reason="No CircPump with the specified id was found.")
    if request.method == 'PATCH':
        # if PATCH add data for circpump
        # can't change pk (name)
        try:
            z.description = request.POST.get('description', default=z.description)
            z.sensor_id = request.POST.get('sensor', default=z.sensor_id)
            z.relay_id = request.POST.get('relay', default=z.relay_id)
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
        # if GET get circpump meta data
        rcircpump = {'count': 1, 'data': [z.as_json()]}
        return JsonResponse(data=rcircpump)


# url options for GET
# targettime=<datetime: targettime> get data <= <targettime>, default is now
# datapts=<int: datapts> get <datapts> sensor reading back from target time, default is 1
# default is to get latest sensor reading for sensor
def circpump_data(request, pump_name):
    # if GET get circpump meta data
    try:
        z = CircPump.objects.get(pk=pump_name)
    except CircPump.DoesNotExist:
        return JsonResponseNotFound(reason="No CircPump with the specified id was found.")
    dseries = {'sensor': get_tempsensor_data(request, z.sensor), 'relay': get_relay_data(request, z.relay)}
    rsensordata = {'count': 1, 'data': dseries}
    return JsonResponse(data=rsensordata)
