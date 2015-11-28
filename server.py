import evdev
import requests
import json
import datetime
import yaml

def main():
  config = load_config()

  dev = evdev.InputDevice(config['device_path'])
  output_line('Initialized - Capturing device: ' + str(dev))

  for event in dev.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
      output_line(event)
      payload = build_payload(event)
      output_line('Sending ' + str(payload) + ' to ' + config['post_url'])
      response = requests.post(config['post_url'], json.dumps(payload))
      output_line(response)

def build_payload(event):
  event = evdev.categorize(event)
  return {
    'code': event.scancode,
    'key': event.keycode[0] if type(event.keycode) == list else event.keycode,
    'state': {0: 'UP', 1: 'DOWN', 2: 'HOLD'}[event.keystate],
    'captured_at': datetime.datetime.fromtimestamp(event.event.timestamp()).isoformat()
  }

def load_config():
  with open('config.yml', 'r') as f:
    return yaml.safe_load(f.read())

def timestamp_s():
  return '[' + str(datetime.datetime.now()) + ']'

def output_line(string):
  print(timestamp_s() + ' ' + str(string))

if __name__ == '__main__':
  main()
