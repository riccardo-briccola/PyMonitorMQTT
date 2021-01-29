import psutil
import math
from Entity import Entity

DOWNLOAD_TOPIC = 'network/bytes_recv'
UPLOAD_TOPIC = 'network/bytes_sent'

# Supports FORMATTED


class NetworkSensor(Entity):
    def Initialize(self):

        self.AddTopic(DOWNLOAD_TOPIC)
        self.AddTopic(UPLOAD_TOPIC)

    def Update(self):
        self.SetTopicValue(DOWNLOAD_TOPIC, psutil.net_io_counters()[
                           1], self.ValueFormatter.TYPE_BYTE)
        self.SetTopicValue(UPLOAD_TOPIC, psutil.net_io_counters()[
                           0], self.ValueFormatter.TYPE_BYTE)
