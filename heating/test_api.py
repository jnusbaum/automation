import requests
import unittest
import pprint
from datetime import datetime
from time import sleep

host = 'http://localhost:8000/automation/api/heating'

zone_name = 'TEST'
in_sensor_name = 'TEST-IN'
out_sensor_name = 'TEST-OUT'


class TestAPI(unittest.TestCase):

    def setUp(self):
        print('setup test')

    def tearDown(self):
        print('teardown test')
        r = requests.delete(f'{host}/zones/{zone_name}')
        r = requests.delete(f'{host}/devices/{out_sensor_name}')
        r = requests.delete(f'{host}/devices/{in_sensor_name}')


    def test(self):
        tcount = 1

        print(f'test {tcount} - add zone')
        data = {'name': zone_name, 'description': 'test zone'}
        r = requests.post(f'{host}/zones', data=data)
        self.assertEqual(requests.codes.created, r.status_code, "bad response = %d" % r.status_code)
        tcount += 1

        print('test %d - get zones' % tcount)
        r = requests.get(f'{host}/zones')
        self.assertEqual(requests.codes.ok, r.status_code, "bad response = %d" % r.status_code)
        data = r.json()
        pprint.pprint(data)
        tcount += 1

        print(f'test {tcount} - get zone')
        r = requests.get(f'{host}/zones/{zone_name}')
        self.assertEqual(requests.codes.ok, r.status_code, "bad response = %d" % r.status_code)
        data = r.json()
        pprint.pprint(data)
        tcount += 1


        print(f'test {tcount} - add sensor')
        data = {'name': in_sensor_name, 'type': 'TEMP', 'address': '', 'description': 'test sensor', 'zone': zone_name}
        r = requests.post(f'{host}/devices', data=data)
        self.assertEqual(requests.codes.created, r.status_code, "bad response = %d" % r.status_code)
        tcount += 1


        print(f'test {tcount} - add sensor')
        data = {'name': out_sensor_name, 'type': 'TEMP', 'address': '', 'description': 'test sensor', 'zone': zone_name}
        r = requests.post(f'{host}/devices', data=data)
        self.assertEqual(requests.codes.created, r.status_code, "bad response = %d" % r.status_code)
        tcount += 1

        print('test %d - get all devices' % tcount)
        r = requests.get(f'{host}/devices')
        self.assertEqual(requests.codes.ok, r.status_code, "bad response = %d" % r.status_code)
        data = r.json()
        pprint.pprint(data)
        tcount += 1

        print(f'test {tcount} - get sensor')
        r = requests.get(f'{host}/devices/{in_sensor_name}')
        self.assertEqual(requests.codes.ok, r.status_code, "bad response = %d" % r.status_code)
        data = r.json()
        pprint.pprint(data)
        tcount += 1

        print(f'test {tcount} - change sensor')
        data = {'address': '0x423e4a'}
        r = requests.patch(f'{host}/devices/{in_sensor_name}', data=data)
        self.assertEqual(requests.codes.no_content, r.status_code, "bad response = %d" % r.status_code)
        tcount += 1

        print(f'test {tcount} - get sensor')
        r = requests.get(f'{host}/devices/{in_sensor_name}')
        self.assertEqual(requests.codes.ok, r.status_code, "bad response = %d" % r.status_code)
        data = r.json()
        pprint.pprint(data)
        tcount += 1

        print('test %d - add data' % tcount)
        tdt = datetime.utcnow()
        tstr = tdt.isoformat()
        data = {'value': '138.2', 'timestamp': tstr}
        r = requests.post(f'{host}/devices/{in_sensor_name}/data', data=data)
        self.assertEqual(requests.codes.created, r.status_code, "bad response = %d" % r.status_code)
        data = {'value': '120.2', 'timestamp': tstr}
        r = requests.post(f'{host}/devices/{out_sensor_name}/data', data=data)
        self.assertEqual(requests.codes.created, r.status_code, "bad response = %d" % r.status_code)
        sleep(10)
        tdt = datetime.utcnow()
        savstr = tstr = tdt.isoformat()
        data = {'value': '136', 'timestamp': tstr}
        r = requests.post(f'{host}/devices/{in_sensor_name}/data', data=data)
        self.assertEqual(requests.codes.created, r.status_code, "bad response = %d" % r.status_code)
        data = {'value': '130', 'timestamp': tstr}
        r = requests.post(f'{host}/devices/{out_sensor_name}/data', data=data)
        self.assertEqual(requests.codes.created, r.status_code, "bad response = %d" % r.status_code)
        sleep(10)
        tdt = datetime.utcnow()
        tstr = tdt.isoformat()
        data = {'value': '143.25', 'timestamp': tstr}
        r = requests.post(f'{host}/devices/{in_sensor_name}/data', data=data)
        self.assertEqual(requests.codes.created, r.status_code, "bad response = %d" % r.status_code)
        data = {'value': '141.25', 'timestamp': tstr}
        r = requests.post(f'{host}/devices/{out_sensor_name}/data', data=data)
        self.assertEqual(requests.codes.created, r.status_code, "bad response = %d" % r.status_code)
        tcount += 1

        print(f'test {tcount} - get data')
        r = requests.get(f'{host}/devices/{in_sensor_name}/data')
        self.assertEqual(requests.codes.ok, r.status_code, "bad response = %d" % r.status_code)
        data = r.json()
        pprint.pprint(data)
        tcount += 1

        print(f'test {tcount} - get data')
        targettime = savstr
        r = requests.get(f'{host}/devices/{in_sensor_name}/data?targettime={targettime}')
        self.assertEqual(requests.codes.ok, r.status_code, "bad response = %d" % r.status_code)
        data = r.json()
        pprint.pprint(data)
        tcount += 1

        print(f'test {tcount} - get data')
        r = requests.get(f'{host}/devices/{in_sensor_name}/data?targettime={targettime}&datapts=2')
        self.assertEqual(requests.codes.ok, r.status_code, "bad response = %d" % r.status_code)
        data = r.json()
        pprint.pprint(data)
        tcount += 1

        print(f'test {tcount} - get data')
        r = requests.get(f'{host}/zones/{zone_name}/data')
        self.assertEqual(requests.codes.ok, r.status_code, "bad response = %d" % r.status_code)
        data = r.json()
        pprint.pprint(data)
        tcount += 1

        print(f'test {tcount} - get data')
        targettime = savstr
        r = requests.get(f'{host}/zones/{zone_name}/data?targettime={targettime}')
        self.assertEqual(requests.codes.ok, r.status_code, "bad response = %d" % r.status_code)
        data = r.json()
        pprint.pprint(data)
        tcount += 1

        print(f'test {tcount} - get data')
        r = requests.get(f'{host}/zones/{zone_name}/data?targettime={targettime}&datapts=2')
        self.assertEqual(requests.codes.ok, r.status_code, "bad response = %d" % r.status_code)
        data = r.json()
        pprint.pprint(data)
        tcount += 1

        print(f'test {tcount} - delete sensor')
        r = requests.delete(f'{host}/devices/{out_sensor_name}')
        self.assertEqual(requests.codes.no_content, r.status_code, "bad response = %d" % r.status_code)
        tcount += 1

        print(f'test {tcount} - delete sensor')
        r = requests.delete(f'{host}/devices/{in_sensor_name}')
        self.assertEqual(requests.codes.no_content, r.status_code, "bad response = %d" % r.status_code)
        tcount += 1

        print(f'test {tcount} - delete zone')
        r = requests.delete(f'{host}/zones/{zone_name}')
        self.assertEqual(requests.codes.no_content, r.status_code, "bad response = %d" % r.status_code)
        tcount += 1

        print(f'test {tcount} - device config')
        r = requests.get(f'{host}/devices/MECHROOM/config')
        self.assertEqual(requests.codes.ok, r.status_code, "bad response = %d" % r.status_code)
        data = r.json()
        pprint.pprint(data)
        tcount += 1


