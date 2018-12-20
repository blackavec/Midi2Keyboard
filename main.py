import sys
import rtmidi
import threading
import pyautogui

from mapper import mapperObject, hotkeyList

class Collector(threading.Thread):
    def __init__(self, device, port):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.port = port
        self.portName = device.getPortName(port)
        self.device = device
        self.quit = False

    def handleMessage(self, midi):
        noteName = midi.getMidiNoteName(midi.getNoteNumber())
        if noteName in mapperObject:
            mappedEvent = mapperObject[noteName]
            pyautogui.hotkey(*mappedEvent)
            print('%s => %s'% (noteName, mappedEvent))

    def run(self):
        self.device.openPort(self.port)
        self.device.ignoreTypes(True, False, True)
        while True:
            if self.quit:
                return

            midi = self.device.getMessage()
            if midi and midi.isNoteOn():
                self.handleMessage(midi)


collectors = []

def plugIn():
    global collectors

    dev = rtmidi.RtMidiIn()
    for i in range(dev.getPortCount()):
        device = rtmidi.RtMidiIn()
        repr(device)
        print('OPENING',dev.getPortName(i))
        collector = Collector(device, i)
        collector.start()
        collectors.append(collector)

plugIn()

print('HIT ENTER TO EXIT')
sys.stdin.read(1)
for c in collectors:
    c.quit = True