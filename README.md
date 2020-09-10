 PDK-sink-node-drvier
 ==========================================================

### This document describes the source code for the 'toIot' iot platform sink node, which is almost used in raspberry Pi  

### This codes runs on a Raspbrerry Pi and communicates with Arduino via mqtt protocol. In this code, Raspberry Pi plays the role of mqtt subscriber and broker , and also plays the role of kafka producer. When various sensor values are received from Arduino and transmitted , the Raspberry Pi, which operates this code, organizes the values with timestamp and sends them to kafka. 

### Raspberry Pi is a sink node that not only communicates with toIot's web server. Raspberry Pi has a seperate web server to communicate by handling requests from toiot's web server    

## Result 
![download](https://user-images.githubusercontent.com/60679342/92687305-3d65e580-f376-11ea-9979-8c457d9bf5b7.gif)




## Installation 

### - Git 
sink node must have an mqtt broker, an mqtt subscriber, and aThe web server that will respond to requests from the backend.

* Mqtt Broker  
 As an MQTT broker,we used eclipse-mosquitto, which is very lightweight and fully supports most functions that an MQTT broker should have. It is also suitable for use on small devices.  
 To install mosquitto, see https://mosquitto.org/download/ for details on installing binaries for various platforms. In this project, we used version 1.6.12

* sink-node-webserver  
  The web server we are going to put on the sink node is based on the flask framework.

  1. Clone the repo  
   ```
  $ git clone https://github.com/SSU-NC/toiot-sink-node-driver
  $ cd toiot-sink-node-driver
  ```

  2. Install the dependencies:  
   ```
  $ pip3 install -r requirements.txt
  ```

## Quick Start 
First start the mqtt broker,Mosquitto:
 ```
  $ mosquitto -v 
  ```
The default port is 1883, but you could change the port by modifiying mosquitto.conf file.

Then start the sink-node web server :
There are three variables you should fill in 
 ```
  $ cd toiot-sink-node-driver
  $ python3 run.py --b='MQTT_BROKER_IP' --k='KAFKA_BROKER_IP' --w='SINK_NODE_WEBSERVER_IP'
  ```






