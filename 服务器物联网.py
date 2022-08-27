#!/usr/bin/python
# -*-coding:utf-8 -*-
import json
import os
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_cors import CORS
os.environ["LANG"] = "en_US.UTF-8"
from flask import Flask, request,render_template

app = Flask(__name__, template_folder='templates')
app.config['MQTT_BROKER_URL'] = 't.yoyolife.fun'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_KEEPALIVE'] = 60
app.config['MQTT_USERNAME'] = 'xxx'
app.config['MQTT_PASSWORD'] = 'xxx'
CORS(app)
mqtt = Mqtt(app)
socketio = SocketIO(app)
@socketio.on('publish')
def handle_publish(json_str):
    data = json.loads(json_str)
    mqtt.publish(data['topic'], data['message'])


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print('on connect')
    mqtt.subscribe('/iot/19/sub/123')


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    print(message.payload)


@app.route('/', methods=['GET'])
def index():
    mqtt.publish("/iot/19/sub/123/test","hi baby")
    return 'welcome'

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=2345, use_reloader=True, debug=True)
