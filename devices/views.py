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
    def __init__(self, data):
        super().__init__(status=HTTPStatus.CREATED, data=data)


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
            rdevices = {'count': 1, 'data': [z.as_json()]}
            return JsonResponseCreated(data=rdevices)
    else:
        # if GET return list of devices_views
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


# url options for GET
def device_config(request, device_name):
    if request.method == 'GET':
        try:
            d = Device.objects.get(pk=device_name)
        except Device.DoesNotExist:
            return JsonResponseNotFound()
    else:
        # not implemented
        return JsonResponseBadRequest()
