
class Actuator:
    def __init__(self):
       pass
    def create_msg(self, actuator, value):
        msg = str(actuator)+',',str(value)
        return(msg)
