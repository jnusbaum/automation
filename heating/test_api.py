import requests
from datetime import datetime
import unittest
import pprint

host = 'http://localhost:8000'

class TestAPI(unittest.TestCase):

    def setUp(self):
        print('setup User test')


    def tearDown(self):
        print('teardown User test')


    def test(self):
        tcount = 1
        print('test %d - add data' % tcount)
        data = {'value-real': '138.2'}
        r = requests.post(f'{host}/api/heating/sensors/MBR-IN/data', data=data)
        self.assertEqual(requests.codes.ok, r.status_code, "bad response = %d" % r.status_code)
        tcount += 1
