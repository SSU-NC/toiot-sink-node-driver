from flask import Flask , Response , make_response,request
from flask import Flask
import paho.mqtt.client as mqtt
from  .healthcheck import Healthcheck
from kafka import KafkaProducer
from kafka.errors import KafkaError , NoBrokersAvailable
import datetime ,os,json ,ast ,copy , time
from  message.mqtt_message import mqtt_messages
from  .http_codes import http_response_code
from bluetooth.bluetooth_message import bluetooth_messages 
import threading,argparse 
from bluetooth import * 

def on_connect(client, userdata, flags, rc):
    print("connected to mqtt broker")
    

def on_subscribe() :   
    print('subscribed')

def on_message(client, userdata, message):
    print ('messaging')


# give message to kafka as kafka producer
def send_message_to_kafka(msg,type):
    if type == "data/mqtt" :
        print("data by mqtt: sending message to kafka : %s" %msg)
        v_topic = msg.topic.split('/')
        kafka_message= topic_manager.kafka_message(v_topic,msg.payload)
        topic_manager.add_ping_state(v_topic[1])             
        print(kafka_message)
        producer.send("sensors",key=v_topic[2].encode(),value= kafka_message)
        
    if type == 'data/bluetooth':
        print("data by bluetooth: sneding message to kafka : %s" %msg)
        v_topic = blt.make_topic(msg)
        kafka_message = topic_manager.kafka_message(v_topic[0:2],v_topic[3])
        topic_manager.add_ping_state(v_topic[1])
        producer.send("sensors",key=v_topic[2].encode(),value= kafka_message)
        
    elif  type == 'ping' :
        print("health check :sending message to kafka : %s" %msg)
        producer.send("healthcheck", msg)    
                 
  



def on_disconnect(client,user_data,rc):
    print("Disconnected")
    client.disconnect()

# check the state of the nodes 
def response_healthcheck():
    while(True) :   
        topic_manager.get_ping_format()
        time.sleep(10)
        topic_manager.ping_message['timestamp'] = str(datetime.datetime.now())[0:19]
        send_message_to_kafka(json.dumps(topic_manager.ping_message).encode('utf-8'),'ping')
        time.sleep(healthcheck.get_time())
        
#receive data from bluetooth connection        
def loop_bluetooth():
    for i in range(len(blt.targets)):
        sockets[i]= BluetoothSocket(RFCOMM)
        sockets[i].connect((blt.targets.values()[i],blt.port))
    while(True):
        try :
            for i in range(len(blt.targets)) :
                recv_data = blt.sockets[i].recv(1024)
                if recv_data is not  None  :
                    print(recv_data)
                    send_message_to_kafka(recv_data,'data/bluetooth')
        except KeyboardInterrupt :
            print('disconnected')
            sock.close()
            print('all done')
    
     
        
#start the raspiwebserver and create objects (Kafka producer,Healthcheck,Mqtt,Bluetooth)
            
app = Flask(__name__)
parser = argparse.ArgumentParser(description='PDK-sink-node-driver opitons')
parser.add_argument('--w',required=True,help='the raspi webserver')
parser.add_argument('--k',required=True,help='kafka')
parser.add_argument('--b',required=True,help='mqtt broker ip')
args= parser.parse_args()
producer = KafkaProducer(bootstrap_servers=args.k,api_version=(0,10,2,0))
topic_manager= mqtt_messages()
client= mqtt.Client()
blt=bluetooth_messages()
app.debug= True
healthcheck = Healthcheck()

# callbacks 
def data_callback(client,userdata,msg) :
    return send_message_to_kafka(msg,"data/mqtt")

# start bluetooth connection with the nodes 
@app.route('/bluetooth')
def bluetooth_run() :
    i=0
    nearby_devices = discover_devices()
    for baddr in nearby_devices :
        print(lookup_name(baddr))
        if  lookup_name(baddr)  in topic_manager.nodes :
            targets[topic_manager.nodes[i]]=baddr   # mac address
            blt.sockets.append(topic_manager.nodes)
            print('device found. target address %s' % target_address)
        i = i+1
    threading.Thread(target=response_healthcheck).start()
    threading.Thread(target= loop_bluetooth).start()
    return http_response_code['success200']
    
#connecting mqtt client to mqtt broker        
@app.route('/mqtt')
def mqtt_run () :  
    threading.Thread(target=response_healthcheck).start() 
    client.on_connect= on_connect
    client.on_message = on_message
    client.on_disconnect= on_disconnect
    client.message_callback_add("data/#",data_callback)    
    client.connect(args.b)
    client.loop_start()
    return http_response_code['success200']    
          
    






# setting interval of the healthcheck time 
@app.route('/health_check/set_time/<time>',methods = ['GET']) 
def healthcheck_set_time() :
    healthcheck.set_time(time)
    return http_response_code['success200']

# interval of the healthcheck time
@app.route('/health_check/get_time', methods = ['GET'])
def healtcheck_get_time():
    healthcheck.get_time() 
    return http_response_code['success200']

# make the format of the topics from the data which toiot server gave
@app.route('/new_topics',methods=['POST'])
def response_getMessageFormat() :
    topic_manager.clear_topics()
    format =json.loads(request.get_data(), encoding='utf-8')
    format=ast.literal_eval(json.dumps(format))
    topic_manager.get_message_format(format)
    client.subscribe(topic_manager.mqtt_topic)
    print(topic_manager.mqtt_topic)
    return http_response_code['success200']
     
# delete sensor            
@app.route('/sensor/<sensor>',methods=['GET','DELETE'])
def delete_sensor(sensor) :
     client.unsubscribe(topic_manager.get_delete_sensor(sensor))
     return http_response_code['success200']
   
# delete arduino board 
@app.route('/node/<node>',methods=['GET','DELETE'])
def delete_node(node) :
     client.unsubscribe(topic_manager.get_delete_node(node))
     return http_response_code['success200']


#error handlers  
@app.errorhandler(400)
def page_bad_request(error) :
    return http_response_code['error400']

@app.errorhandler(401)
def page_unauthorized(error) :
    return http_response_code['error401']

@app.errorhandler(403)
def page_forbidden(error) :
    return http_response_code['error403']


@app.errorhandler(404)
def page_not_found(error) :
    return http_response_code['error404']

@app.errorhandler(408)
def page_timeout(error) :
    return http_response_code['error408']




