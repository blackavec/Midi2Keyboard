import sys
import rtmidi
import threading

from mapper import mapperObject, hotkeyList
from pyautogui import press, hotkey, keyDown, keyUp

def handleMessage(midi):
    if midi.isNoteOn():
        noteName = midi.getMidiNoteName(midi.getNoteNumber())
        mappedEvent = mapperObject[noteName]

        # send the event to keyboard
        hotkeys = []
        keys = []
        for event in mappedEvent:
            if event in hotkeyList:
                hotkeys.insert(0, event)
                keyDown(event)
                print('hold down %s' % event)
                continue

            print('press %s' % event)
            press(event)

        for key in hotkeys:
          keyUp(key)
          print('key up %s' % key)

class Collector(threading.Thread):
    def __init__(self, device, port):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.port = port
        self.portName = device.getPortName(port)
        self.device = device
        self.quit = False

    def run(self):
        self.device.openPort(self.port)
        self.device.ignoreTypes(True, False, True)
        while True:
            if self.quit:
                return

            msg = self.device.getMessage()
            if msg:
                handleMessage(msg)


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