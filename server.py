import evdev
import requests
import json
import datetime

# TODO: These should go into a configuration file
DEVICE_PATH = '/dev/input/event0'
URL = 'http://requestb.in/1b2bo6r1'

dev = evdev.InputDevice(DEVICE_PATH)
print('Capturing device: ' + str(dev))

for event in dev.read_loop():
  if event.type == evdev.ecodes.EV_KEY:
    event = evdev.categorize(event)
    print(str(datetime.datetime.now()) + ' - ' + str(event))
    payload = {
      'code': event.scancode,
      'key': event.keycode[0] if type(event.keycode) == list else event.keycode,
      'state': {0: 'up', 1: 'down', 2: 'hold'}[event.keystate]
    }
    print(payload)
    r = requests.post(URL, json.dumps(payload))
    print(str(datetime.datetime.now()) + ' - ' + str(r))
