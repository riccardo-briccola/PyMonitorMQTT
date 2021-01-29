import psutil
from Entity import Entity
import signal, sys

TOPIC_STATE = 'state'


class StateSensor(Entity):
    def Initialize(self):
        self.AddTopic(TOPIC_STATE)
        signal.signal(signal.SIGINT, self.ExitSignal)


    def Update(self):
        self.SetTopicValue(TOPIC_STATE, self.consts.ONLINE_STATE)

    def SendOfflineState(self):
        self.mqtt_client.SendTopicData(self.SelectTopic(TOPIC_STATE),self.consts.OFFLINE_STATE)

    def ExitSignal(self,sig, frame):
        # Before exiting I send an offline message to the state_topic if prese
        print("\r", end="") # This removes the Control-C symbol (^C)
        self.Log(self.Logger.LOG_INFO,'Let me send the Offline state message')
        self.SendOfflineState()
        self.Log(self.Logger.LOG_INFO,"All done, goodbye !")
        sys.exit(0)
        
    def ManageDiscoveryData(self,payload_data): # Don't send unavailable config for this state, it's okay the Oflline state
        payload_data[0]['payload']['availability_topic'] = ""  
        payload_data[0]['payload']['payload_available'] = ""
        payload_data[0]['payload']['payload_not_available'] = ""
        return payload_data