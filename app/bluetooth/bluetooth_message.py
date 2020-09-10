#simple class for bluetooth 
#target_names are the names of the bluetooth module which are connected with the raspi
#targets is a dictionary which contains the pairs of names and the address of the bluetooth module


class bluetooth_messages :
    target_names=[]
    targets={}
    sockets=[]
    
    
    def make_topic(self,msg) :
        msg= msg.decode('utf-8')
        v_topic=msg.split('/')
        return v_topic
        
    
         
    
    
    