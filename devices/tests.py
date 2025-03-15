import requests
import unittest
import pprint
from datetime import datetime
from time import sleep

host = 'http://localhost:8000/automation/devices/api'


class TestAPI(unittest.TestCase):
    in_sensor_name = 'TEST-IN'
    out_sensor_name = 'TEST-OUT'
    device_name = 'TEST'
    relay_name = 'TEST'
    ow_pin = 2
    ow_id = 0

    def setUp(self):
        print('setup test')


    def tearDown(self):
        print('teardown test')
        r = requests.delete(f'{host}/tempsensors/{self.out_sensor_name}')
        r = requests.delete(f'{host}/tempsensors/{self.in_sensor_name}')
        r = requests.delete(f'{host}/onewireinterfaces/{self.ow_id}')
        r = requests.delete(f'{host}/relays/{self.relay_name}')
        r = requests.delete(f'{host}/devices/{self.device_name}')


    def test(self):
        tcount = 1

        # create a device
        print(f'test {tcount} - create device')
        data = {'name': self.device_name}
        r = requests.post(f'{host}/devices/', data=data)
        self.assertEqual(requests.codes.created, r.status_code, "bad response = %d" % r.status_code)
        data = r.json()
        pprint.pprint(data)
        tcount += 1

        # create a one wire interface
        print(f'test {tcount} - create one wire interface')
        data = {'pin': self.ow_pin, 'device': self.device_name}
        r = requests.post(f'{host}/onewireinterfaces/', data=data)
        self.assertEqual(requests.codes.created, r.status_code, "bad response = %d" % r.status_code)
        data = r.json()
        pprint.pprint(data)
        ow = data['data'][0]
        self.ow_id = ow['id']
        tcount += 1

        # access the device relationship
        path = ow['relationships']['device']
        print(f'test {tcount} - access device relationship')
        r = requests.get(f'{host}{path}')
        self.assertEqual(requests.codes.ok, r.status_code, "bad response = %d" % r.status_code)
        data = r.json()
        pprint.pprint(data)
        tcount += 1

        print(f'test {tcount} - add sensor')
        data = {'name': self.in_sensor_name, 'interface': self.ow_id, 'description': 'test sensor'}
        r = requests.post(f'{host}/tempsensors/', data=data)
        self.assertEqual(requests.codes.created, r.status_code, "bad response = %d" % r.status_code)
        data = r.json()
        pprint.pprint(data)
        tcount += 1

        print(f'test {tcount} - add sensor')
        data = {'name': self.out_sensor_name, 'interface': self.ow_id, 'description': 'test sensor'}
        r = requests.post(f'{host}/tempsensors/', data=data)
        self.assertEqual(requests.codes.created, r.status_code, "bad response = %d" % r.status_code)
        data = r.json()
        pprint.pprint(data)
        tcount += 1

        print('test %d - get all tempsensors' % tcount)
        r = requests.get(f'{host}/tempsensors/')
        self.assertEqual(requests.codes.ok, r.status_code, "bad response = %d" % r.status_code)
        data = r.json()
        pprint.pprint(data)
        tcount += 1

        print(f'test {tcount} - get sensor')
        r = requests.get(f'{host}/tempsensors/{self.in_sensor_name}/')
        self.assertEqual(requests.codes.ok, r.status_code, "bad response = %d" % r.status_code)
        data = r.json()
        pprint.pprint(data)
        tcount += 1

        print(f'test {tcount} - change sensor')
        data = {'address': '0x423e4a'}
        r = requests.patch(f'{host}/tempsensors/{self.in_sensor_name}/', data=data)
        self.assertEqual(requests.codes.no_content, r.status_code, "bad response = %d" % r.status_code)
        tcount += 1

        print(f'test {tcount} - get sensor')
        r = requests.get(f'{host}/tempsensors/{self.in_sensor_name}/')
        self.assertEqual(requests.codes.ok, r.status_code, "bad response = %d" % r.status_code)
        data = r.json()
        pprint.pprint(data)
        tcount += 1

        print('test %d - add data' % tcount)
        tdt = datetime.utcnow()
        tstr = tdt.isoformat()
        data = {'value': '138.2', 'timestamp': tstr}
        path = f'{host}/tempsensors/{self.in_sensor_name}/data/'
        r = requests.post(path, data=data)
        self.assertEqual(requests.codes.created, r.status_code, "bad response = %d" % r.status_code)
        data = {'value': '120.2', 'timestamp': tstr}
        r = requests.post(f'{host}/tempsensors/{self.out_sensor_name}/data/', data=data)
        self.assertEqual(requests.codes.created, r.status_code, "bad response = %d" % r.status_code)
        sleep(10)
        tdt = datetime.utcnow()
        savstr = tstr = tdt.isoformat()
        data = {'value': '136', 'timestamp': tstr}
        r = requests.post(f'{host}/tempsensors/{self.in_sensor_name}/data/', data=data)
        self.assertEqual(requests.codes.created, r.status_code, "bad response = %d" % r.status_code)
        data = {'value': '130', 'timestamp': tstr}
        r = requests.post(f'{host}/tempsensors/{self.out_sensor_name}/data/', data=data)
        self.assertEqual(requests.codes.created, r.status_code, "bad response = %d" % r.status_code)
        sleep(10)
        tdt = datetime.utcnow()
        tstr = tdt.isoformat()
        data = {'value': '143.25', 'timestamp': tstr}
        r = requests.post(f'{host}/tempsensors/{self.in_sensor_name}/data/', data=data)
        self.assertEqual(requests.codes.created, r.status_code, "bad response = %d" % r.status_code)
        data = {'value': '141.25', 'timestamp': tstr}
        r = requests.post(f'{host}/tempsensors/{self.out_sensor_name}/data/', data=data)
        self.assertEqual(requests.codes.created, r.status_code, "bad response = %d" % r.status_code)
        tcount += 1

        print(f'test {tcount} - get data')
        r = requests.get(f'{host}/tempsensors/{self.in_sensor_name}/data/')
        self.assertEqual(requests.codes.ok, r.status_code, "bad response = %d" % r.status_code)
        data = r.json()
        pprint.pprint(data)
        tcount += 1

        print(f'test {tcount} - get data')
        targettime = savstr
        r = requests.get(f'{host}/tempsensors/{self.in_sensor_name}/data/?targettime={targettime}')
        self.assertEqual(requests.codes.ok, r.status_code, "bad response = %d" % r.status_code)
        data = r.json()
        pprint.pprint(data)
        tcount += 1

        print(f'test {tcount} - get data')
        r = requests.get(f'{host}/tempsensors/{self.in_sensor_name}/data/?targettime={targettime}&datapts=2')
        self.assertEqual(requests.codes.ok, r.status_code, "bad response = %d" % r.status_code)
        data = r.json()
        pprint.pprint(data)
        tcount += 1

        print(f'test {tcount} - delete sensor')
        r = requests.delete(f'{host}/tempsensors/{self.out_sensor_name}/')
        self.assertEqual(requests.codes.no_content, r.status_code, "bad response = %d" % r.status_code)
        tcount += 1

        print(f'test {tcount} - delete sensor')
        r = requests.delete(f'{host}/tempsensors/{self.in_sensor_name}/')
        self.assertEqual(requests.codes.no_content, r.status_code, "bad response = %d" % r.status_code)
        tcount += 1

        print(f'test {tcount} - device config')
        r = requests.get(f'{host}/devices/{self.device_name}/config/')
        self.assertEqual(requests.codes.ok, r.status_code, "bad response = %d" % r.status_code)
        data = r.json()
        pprint.pprint(data)
        tcount += 1


