import json
import datetime
from .http_codes import http_response_code

'''
Create a topic manager to manage overall topics
The types of topics are broadly divided into a topic to receive data transmitted from the
Arduino board and a topic to check the ping status.
Other topics can be additionally managed
'''
class mqtt_messages:


    
    nodes =[]
    ping_receive= []
    mqtt_topic =[]
    topics = []
    ping_message= {}
    vos = 0
    delete_topic =[]
    def kafka_message(self,v_topic,payload) :
        kafka_msg ={}
        kafka_msg['nid'] = v_topic[1]
        payload = payload.split(',')
        kafka_msg['values']= map(float, payload)
        kafka_msg['timestamp'] = str(datetime.datetime.now())[0:19]
        _str = json.dumps(kafka_msg).encode('utf-8')
        return _str 
        
    def set_vos(self,number) :
        self.vos = number


    def get_message_format(self,format) :
        self.clear_topics()
        topics = format[0]
        topics = topics['topics']
        for i in range(len(topics)):
            topic = "data/" + topics[i]['node_uuid'] + "/" + topics[i]['sensor_uuid']
            if topics[i]['node_uuid'] not in self.nodes :
                self.nodes.append(topics[i]['node_uuid'])
                self.ping_receive.append(("ping/"+topics[i]['node_uuid']))
            self.add_mqtt_topic(topic,self.vos)
            

    def get_ping_format(self) :
        self.ping_message['timestamp'] = 0
        self.ping_message['state']=[]
        for i in range(len(self.nodes)):
            temp =  {
             'n_uuid' : self.nodes[i],
             'state' : False
            }
            self.ping_message['state'].append(temp)
           

    def add_ping_state(self,topic):  
        for i in range(len( self.ping_message['state'])):
            if (topic == self.ping_message['state'][i]['n_uuid']):
                self.ping_message['state'][i]['state']= True 
        
          

    def add_mqtt_topic(self,topic,vos):
        self.topics.append(topic)
        topic = (topic,vos)
        self.mqtt_topic.append(topic)
        
    def get_delete_node(self,nodeid):
        self.delete_topic =[]
        for i in range (len(self.topics)):
           v_topic=self.topics[i].split('/')
           if (v_topic[1] == nodeid) :
            self.nodes.remove(nodeid)
            self.delete_topic.append(self.topics[i])
            print(self.delete_topic)  
        return self.delete_topic 
          
        
    
    def get_delete_sensor(self,sensorid):           
        for i in range (len(self.topics)):
            v_topic =self.topics[i].split('/')
            if (v_topic[2] == sensorid) :
                delete_topic= self.topics[i]   
                return delete_topic
        return  sensor
       
    



    def clear_topics(self):
        self.mqtt_topic =[]
        self.topics = []             
        self.nodes =[]
        self.ping_receive = []
        self.ping_message_format = []
    