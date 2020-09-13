import ast
import datetime
import json
import time

import paho.mqtt.client as mqtt
from flask import Flask
from flask import request
from kafka import KafkaProducer
from message.mqtt_message import MqttMessages

from .healthcheck import HealthCheck
from .http_codes import http_response_code
from .setup import args


def on_connect(client, userdata, flags, rc):
    print("connected to mqtt broker")


def on_subscribe():
    print('subscribed')


def on_message(client, userdata, message):
    print('messaging')


# give message to kafka as kafka producer
def send_message_to_kafka(msg):
    v_topic = msg.topic.split('/')
    payload = msg.payload.decode().split(',')
    kafka_message = topic_manager.kafka_message(v_topic, payload)
    if topic_manager.sensor_check(v_topic[1], payload):
        if health_check.get_health_check_mode():
            topic_manager.add_ping_state(v_topic[1])
        print("data by mqtt: sending message to kafka : %s" % msg)
        print(kafka_message)
        producer.send("sensors", kafka_message)


# callbacks
def data_callback(client, userdata, msg):
    return send_message_to_kafka(msg)


# connecting mqtt client to mqtt broker
def mqtt_run():
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.message_callback_add("data/#", data_callback)
    client.connect(args.b)
    client.loop_start()
    return http_response_code['success200']


def on_disconnect(client, user_data, rc):
    print("Disconnected")
    client.disconnect()


# start the node webserver

app = Flask(__name__)
producer = KafkaProducer(bootstrap_servers=args.k, api_version=(0, 10, 2, 0))
topic_manager = MqttMessages()
client = mqtt.Client()
app.debug = True
health_check = HealthCheck()
mqtt_run()


# check the state of the nodes
@app.route('/health-check')
def response_health_check():
    # making the ping message format by the topics
    topic_manager.get_ping_format()
    health_check.set_health_check_mode(True)
    time.sleep(health_check.get_time())
    topic_manager.ping_message['timestamp'] = str(datetime.datetime.now())[0:19]
    health_check.set_health_check_mode(False)
    print(topic_manager.ping_message)
    return json.dumps(topic_manager.ping_message).encode('utf-8')


# connecting mqtt client to mqtt broker
def mqtt_run():
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.message_callback_add("data/#", data_callback)
    client.connect(args.b)
    client.loop_start()
    return http_response_code['success200']


# setting interval of the health check time
@app.route('/health-check/set_time/<time>', methods=['GET'])
def health_check_set_time():
    health_check.set_time(time)
    return http_response_code['success200']


# interval of the health check time
@app.route('/health-check/time', methods=['GET'])
def health_check_get_time():
    health_check.get_time()
    return http_response_code['success200']


# make the format of the topics from the data which toiot server gave
@app.route('/topics', methods=['POST'])
def response_getMessageFormat():
    topic_manager.clear_topics()
    temp = json.loads(request.get_data().decode())
    topic_manager.get_message_format(temp)
    client.subscribe(topic_manager.mqtt_topic)
    print(topic_manager.mqtt_topic)
    return http_response_code['success200']


# delete sensor            
@app.route('/sensors/<sensor>', methods=['GET', 'DELETE'])
def delete_sensor(sensor):
    client.unsubscribe(topic_manager.get_delete_sensor(sensor))
    return http_response_code['success200']


# delete arduino board 
@app.route('/node/<node>', methods=['GET', 'DELETE'])
def delete_node(node):
    client.unsubscribe(topic_manager.get_delete_node(node))
    return http_response_code['success200']


# error handlers
@app.errorhandler(400)
def page_bad_request(error):
    return http_response_code['error400']


@app.errorhandler(401)
def page_unauthorized(error):
    return http_response_code['error401']


@app.errorhandler(403)
def page_forbidden(error):
    return http_response_code['error403']


@app.errorhandler(404)
def page_not_found(error):
    return http_response_code['error404']


@app.errorhandler(408)
def page_timeout(error):
    return http_response_code['error408']
