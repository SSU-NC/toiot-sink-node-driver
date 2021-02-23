import json

class Actuator:
    def __init__(self):
        pass
    def send_req(self,client, json_data):
        print('Send ActuatorReq to node ', str(json_data['nid']), ' ...')
        client.publish('command/downlink/ActuatorReq/'+str(json_data['nid']), json.dumps(json_data).encode('utf-8'), qos=2)
