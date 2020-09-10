# Toiot Sink Node Driver
This document describes the source code for the `toIot` iot platform sink node, which is almost used in embedded board installed Linux OS. This codes communicates with Arduino via mqtt protocol. In this code, sink node plays the role of mqtt subscriber and broker, and also plays the role of kafka producer. When various sensor values are received from Arduino and transmitted, the sink node which operates this code organizes the values with timestamp and sends them to kafka. Sink node can communicate with toIot's web server.

## Result 
![download](https://user-images.githubusercontent.com/60679342/92687305-3d65e580-f376-11ea-9979-8c457d9bf5b7.gif)

## Installation 
1. Clone the repo  
  ```
  $ git clone https://github.com/SSU-NC/toiot-sink-node-driver
  $ cd toiot-sink-node-driver
  ```
2. Install the dependencies
  ```
  $ pip3 install -r requirements.txt
  ```
3. install [eclipse-mosquitto](https://mosquitto.org/download/). In this project, we used version 1.6.12.

### Run 
```
$ cd toiot-sink-node-driver/app
$ python3 run.py --b='MQTT_BROKER_IP' --k='KAFKA_BROKER_IP' --w='SINK_NODE_WEBSERVER_IP'
```







