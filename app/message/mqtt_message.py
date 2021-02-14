import json
import datetime
from server.http_codes import http_response_code

'''
Create a topic manager to manage overall topics
The types of topics are broadly divided into a topic to receive data transmitted from the
Arduino board and a topic to check the ping status.
Other topics can be additionally managed
'''


class MqttMessages:
    sensors = []
    nodes = []
    ping_receive = []
    mqtt_topic = []
    topics = []
    ping_message = {}
    vos = 0
    delete_topic = []

    def __init__(self):
        self.ping_message_format = []

    def kafka_message(self, v_topic, payload):
        payload[1:] = list(map(float, payload[1:]))
        kafka_msg = {'node_id': int(v_topic[1]), 'sensor_id': int(payload[0]), 'values': payload[1:],
                     'timestamp': str(datetime.datetime.now())[0:19]}
        temp = json.dumps(kafka_msg).encode('utf-8')
        return temp

    def set_vos(self, number):
        self.vos = number
    
    def get_nodes(self):
        return self.nodes
    def add_node(self, nodeid):
        self.nodes.append(nodeid)

    def get_message_format(self, format):
        self.clear_topics()
        temp = format['nodes']
        self.sensors = temp
        for i in range(len(temp)):
            temp[i]['id'] = str(temp[i]['id'])
            topic = "data/" + temp[i]['id']
            self.nodes.append(int(temp[i]['id']))
            self.ping_receive.append(("ping/" + temp[i]['id']))
            self.add_mqtt_topic(topic, self.vos)

    def sensor_check(self, nodeid, payload):
        for sensor in self.sensors:
            if sensor['id'] == nodeid:
                for sensorid in sensor['sensors']:
                    if str(sensorid['id']) == payload[0]:
                        return True
        return False
    '''
    def get_ping_format(self):
        self.ping_message['timestamp'] = 0
        self.ping_message['state'] = []
        for i in range(len(self.nodes)):
            temp = {
                'n_uuid': self.nodes[i],
                'state': False
            }
            self.ping_message['state'].append(temp)

    def add_ping_state(self, topic):
        for elem in self.ping_message['state']:
            if int(topic) == elem['n_uuid']:
                elem['state'] = True
    '''
    def add_mqtt_topic(self, topic, vos):
        self.topics.append(topic)
        topic = (topic, vos)
        self.mqtt_topic.append(topic)

    def get_delete_node(self, nodeid):
        self.delete_topic = []
        for i in range(len(self.topics)):
            v_topic = self.topics[i].split('/')
            if v_topic[1] is nodeid:
                self.nodes.remove(nodeid)
                self.delete_topic.append(self.topics[i])
                print(self.delete_topic)
        return self.delete_topic

    def get_delete_sensor(self, sensorid):
        for i in range(len(self.topics)):
            v_topic = self.topics[i].split('/')
            if v_topic[2] == sensorid:
                delete_topic = self.topics[i]
                return delete_topic
        return v_topic

    def clear_topics(self):
        self.mqtt_topic = []
        self.topics = []
        self.nodes = []
        self.ping_receive = []
        self.sensors = []
