import requests
import unittest
import pprint
from datetime import datetime

host = 'http://192.168.0.104:5000'

class TestAPI(unittest.TestCase):

    def setUp(self):
        print('setup test')


    def tearDown(self):
        print('teardown test')


    def test(self):
        tcount = 1
        print('test %d - add data' % tcount)
        data = {'value-real': '138.2', 'timestamp': datetime.today().strftime("%Y-%m-%d-%H-%M-%S")}
        r = requests.post(f'{host}/sensors/MBR-IN/data', data=data)
        self.assertEqual(requests.codes.created, r.status_code, "bad response = %d" % r.status_code)
        tcount += 1

        print('test %d - get sensors' % tcount)
        r = requests.get(f'{host}/sensors')
        self.assertEqual(requests.codes.ok, r.status_code, "bad response = %d" % r.status_code)
        data = r.json()
        pprint.pprint(data)
        tcount += 1
