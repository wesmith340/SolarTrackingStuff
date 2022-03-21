from dataclasses import dataclass
from datetime import datetime
from flask import Flask, jsonify

import os
from sqlite3 import Timestamp
from sqlalchemy import Column, Integer, create_engine, Float, TIMESTAMP
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base
from datetime import datetime
from flask_heroku import Heroku

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql://')

heroku = Heroku(app)

db = SQLAlchemy(app)

@dataclass
class Data(db.Model):
    __tablename__ = 'solar_data'
    id = db.Column(Integer, primary_key=True)
    batt_voltage = db.Column(Float)
    pv_voltage = db.Column(Float)
    charge_current = db.Column(Float)
    load_amps = db.Column(Float)
    timestamp = db.Column(TIMESTAMP)

    def __init__(self, batt_voltage, pv_voltage, charge_current, load_amps):
        self.batt_voltage = batt_voltage
        self.pv_voltage = pv_voltage
        self.charge_current = charge_current
        self.load_amps = load_amps
        self.timestamp = datetime.now()



@app.route('/', methods=['GET'])
def index():
    return 'Welcome to the SVSU Solar app'


@app.route('/solar/', methods=['GET'])
def get_data():
    data = Data.query.first()
    if data is not None:
        return jsonify({
            'batt_voltage':data.batt_voltage,
            'pv_voltage':data.pv_voltage,
            'charge_current':data.charge_current,
            'load_amps':data.load_amps,
            'timestamp':data.timestamp
            })
    else:
        return jsonify({'error': 'Solar data is offline'})

@app.route('/pushdata/<batt_voltage>/<pv_voltage>/<charge_current>/<load_amps>/', methods=['GET'])
def post_data(batt_voltage, pv_voltage, charge_current,load_amps):
    data = Data.query.first()
    if data is not None:
        data.batt_voltage = batt_voltage
        data.pv_voltage = pv_voltage
        data.charge_current = charge_current
        data.load_amps = load_amps
        data.timestamp = datetime.now()
        # Hello
    else:
        data = Data(batt_voltage, pv_voltage, charge_current, load_amps)
        db.session.add(data)

    db.session.commit()
    
        
    return 'data pushed'

db.create_all()

if __name__ == '__main__':
    app.run()
