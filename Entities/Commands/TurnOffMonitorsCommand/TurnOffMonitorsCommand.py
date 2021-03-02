import subprocess
import ctypes
import os as sys_os
from Entities.Entity import Entity
from ctypes import *

TOPIC = 'turn_off_monitors_command'

class TurnOffMonitorsCommand(Entity):
    def Initialize(self):
        self.SubscribeToTopic(TOPIC)

    def PostInitialize(self):
        self.os = self.GetOS()

    def Callback(self, message):
        if self.os == 'Windows':
            ctypes.windll.user32.SendMessageA(0xFFFF, 0x0112, 0xF170, 2)
        elif self.os == 'Linux':
            # Check if X11 or something else
            if sys_os.environ.get('DISPLAY'):
                command = 'xset dpms force off'
                subprocess.Popen(command.split(), stdout=subprocess.PIPE)
            else:
                raise Exception(
                    'The Turn Off Monitors command is not available for this Linux Window System')

        else:
            raise Exception(
                'The Turn Off Monitors command is not available for this Operating System')

    def GetOS(self):
        # Get OS from OsSensor and get temperature based on the os
        os = self.FindEntity('Os')
        if os:
            if not os.postinitializeState: # I run this function in post initialize so the os sensor might not be ready
                os.PostInitialize()
            os.CallUpdate()
            return os.GetTopicValue()


