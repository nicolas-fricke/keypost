import evdev
import requests
import json
import datetime
import yaml

with open('config.yml', 'r') as f:
  config = yaml.safe_load(f.read())

dev = evdev.InputDevice(config['device_path'])
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
    r = requests.post(config['post_url'], json.dumps(payload))
    print(str(datetime.datetime.now()) + ' - ' + str(r))
