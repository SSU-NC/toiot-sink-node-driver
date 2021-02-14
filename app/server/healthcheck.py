"""
health checking
The status of the Arduino boards, which are mqtt publishers,
are checked every 30 seconds by default and the information is sent to kafka.
healthcheck.py can change the default time of 30 seconds as requested by the web server
"""
from .config import dev_info
import json

class HealthCheck:

    # default time
    def __init__(self):
        self.target_nodelist={}
        self.time = 30
        self.ping_message = "ping time:" + str(self.time)
        self.health_check_mode = False
    def set_time(self, time):
        self.time = time

    def get_time(self):
        return self.time

    def get_health_check_mode(self):
        return self.health_check_mode

    def set_health_check_mode(self, mode):
        self.health_check_mode = mode
        
    def setup_target_nodelist(self, nodelist):
        self.target_nodelist = dict()
        for nodeid in nodelist:
            self.target_nodelist[nodeid] = False

    def set_node_state(self, nodeid, state):
        if int(nodeid) in self.target_nodelist:
            self.target_nodelist[int(nodeid)] = state
            return True #success
        else:
            return False #error

    def create_msg(self):
        json_msg = dict()
        state_list = list()
        json_msg['sid'] = dev_info.get_id()
    
        for nodeid in self.target_nodelist: #nodeid is key
            state_list += [{'nid':nodeid, 'state':self.target_nodelist[nodeid]}]
        json_msg['state'] = state_list
        
        return json.dumps(json_msg).encode('UTF-8')

