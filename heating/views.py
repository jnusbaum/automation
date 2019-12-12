from django.http import HttpResponse
from django.shortcuts import render
import requests

host = 'http://192.168.0.134'

# Create your views here.
def index(request):
    # fake samples
    # samples = [
    #     {'name': 'MBR-IN', 'timestamp': '2019-12-12-14-22-34', 'value': '142.45'},
    #     {'name': 'MBR-OUT', 'timestamp': '2019-12-12-14-22-34', 'value': '102.00'},
    #     {'name': 'OFFICE-IN', 'timestamp': '2019-12-12-14-22-34', 'value': '94.50'},
    #     {'name': 'OFFICE-OUT', 'timestamp': '2019-12-12-14-22-34', 'value': '92.67'},
    # ]
    # get samples from data server
    # first get sensors
    r = requests.get(f'{host}/sensors')
    if (requests.codes.ok != r.status_code):
        # error
        return HttpResponse(status_code=r.status_code)
    data = r.json()
    sensors = data['data']
    samples = []
    for sensor in sensors:
        r = requests.get(f"{host}/sensors/{sensor['id']}/data")
        if (requests.codes.ok != r.status_code):
            # error
            return HttpResponse(status_code=r.status_code)
        data = r.json()
        for sample in data['data']:
            samples.append({'name': sensor['id'], 'timestamp': sample['attributes']['timestamp'], 'value': sample['attributes']['value_real']})
    return render(request, 'heating/heating-dashboard.html', {'samples': samples})
