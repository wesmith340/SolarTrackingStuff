from time import sleep
from urllib.parse import urljoin
from serial import Serial

import requests

import sys
sys.path.append('/home/pi/tracer/python')
from tracer import Tracer, TracerSerial, QueryCommand

WEB_URL = 'https://svsusolardata.herokuapp.com'
SLEEP_TIME = 30000

port = Serial('/dev/ttyAMA0', 9600, timeout=1)
port.flushInput()
port.flushOutput()
tracer = Tracer(0x16)
t_ser = TracerSerial(tracer, port)
query = QueryCommand()

def post_data():
    try:
        t_ser.send_command(query)
        data = t_ser.receive_result()

    

        data = {'batt_voltage':data.batt_voltage,
            'pv_voltage':data.pv_voltage,
            'charge_current':data.charge_current,
            'load_amps':data.load_amps}

        # data = {'batt_voltage':10,
        #     'pv_voltage':5,
        #     'charge_current':5,
        #     'load_amps':10}


        url = f"{WEB_URL}/pushdata/{data['batt_voltage']}/{data['pv_voltage']}/{data['charge_current']}/{data['load_amps']}"
        response = requests.get(url=url)
        print(response)


    except (IndexError, IOError) as e:
        port.flushInput()
        port.flushOutput()
        return jsonify({'error': e.message}), 503

while (True):
    post_data()
    sleep(SLEEP_TIME)