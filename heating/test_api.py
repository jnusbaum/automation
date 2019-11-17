import requests
import unittest
import pprint

host = 'http://192.168.0.134:8000'

class TestAPI(unittest.TestCase):

    def setUp(self):
        print('setup test')


    def tearDown(self):
        print('teardown test')


    def test(self):
        tcount = 1

        print('test %d - get sensors' % tcount)
        r = requests.get(f'{host}/api/heating/sensors')
        self.assertEqual(requests.codes.ok, r.status_code, "bad response = %d" % r.status_code)
        data = r.json()
        pprint.pprint(data)
        tcount += 1

        sensor_name = 'MBR-IN'
        print(f'test {tcount} - get sensor')
        r = requests.get(f'{host}/api/heating/sensors/{sensor_name}')
        self.assertEqual(requests.codes.ok, r.status_code, "bad response = %d" % r.status_code)
        data = r.json()
        pprint.pprint(data)
        tcount += 1

        # print(f'test {tcount} - add sensor')
        # data = {'name': 'TEST', 'type': 'TEMP', 'address':, 'description': }
        # r = requests.post(f'{host}/api/heating/sensors', data=data)
        # self.assertEqual(requests.codes.created, r.status_code, "bad response = %d" % r.status_code)
        # tcount += 1

        print('test %d - add data' % tcount)
        data = {'value-real': '138.2'}
        r = requests.post(f'{host}/api/heating/sensors/{sensor_name}/data', data=data)
        self.assertEqual(requests.codes.created, r.status_code, "bad response = %d" % r.status_code)
        tcount += 1
