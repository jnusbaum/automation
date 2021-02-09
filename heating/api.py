from heating.models import *
from sensors.api import *

MAX_TEMP_MOVE = 25
MIN_TEMP = 30


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


def zones(request):
    if request.method == 'POST':
        try:
            zone_name = request.POST['name']
        except KeyError:
            return JsonResponseBadRequest(reason="No name parameter supplied.")
        # if POST add new zone
        try:
            Zone.objects.get(pk=zone_name)
            return JsonResponseBadRequest(reason="Zone with supplied name already exists.")
        except Zone.DoesNotExist:
            description = request.POST.get('description', default=None)
            z = Zone(name=zone_name, description=description)
            z.save()
            return JsonResponseCreated()
    else:
        # if GET return list of zones
        zns = Zone.objects.all().order_by('name')
        rzones = {'count': len(zns), 'data': [z.as_json() for z in zns]}
        return JsonResponse(data=rzones)


def zone(request, zone_name):
    try:
        z = Zone.objects.get(pk=zone_name)
    except Zone.DoesNotExist:
        return JsonResponseNotFound(reason="No Zone with the specified id was found.")
    if request.method == 'PATCH':
        # if PATCH add data for zone
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
        # if GET get zone meta data
        rzone = {'count': 1, 'data': [z.as_json()]}
        return JsonResponse(data=rzone)


def sensors_for_zone(zone_name):
    # if GET get zone meta data
    try:
        z = Zone.objects.get(pk=zone_name)
    except Zone.DoesNotExist:
        return JsonResponseNotFound(reason="No Zone with the specified id was found.")
    # sensors for zone
    rsensors = {'count': len(z.sensors), 'data': [s.as_json for s in z.sensors]}
    return JsonResponse(data=rsensors)


# url options for GET
# targettime=<datetime: targettime> get data <= <targettime>, default is now
# datapts=<int: datapts> get <datapts> sensor reading back from target time, default is 1
# default is to get latest sensor reading for sensor
def zone_data(request, zone_name):
    # if GET get zone meta data
    try:
        z = Zone.objects.get(pk=zone_name)
    except Zone.DoesNotExist:
        return JsonResponseNotFound(reason="No Zone with the specified id was found.")
    dseries = {}
    for s in z.sensors.all():
        dseries[s.name] = get_sensor_data(request, s)
    rsensordata = {'count': 1, 'data': dseries}
    return JsonResponse(data=rsensordata)

