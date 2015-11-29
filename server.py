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
      if is_to_be_logged(payload, config):
        url = build_url(config['post_url'], payload)
        output_line('Sending ' + str(payload) + ' to ' + url)
        response = requests.post(url, json.dumps(payload))
        output_line(response)
      else:
        output_line('Not sending ' + str(payload) + ' since it is not whitelisted')

def load_config():
  with open('config.yml', 'r') as f:
    return yaml.safe_load(f.read())

def build_url(base_url, payload):
  return base_url % payload

def build_payload(event):
  event = evdev.categorize(event)
  return {
    'code': event.scancode,
    'key': event.keycode[0] if type(event.keycode) == list else event.keycode,
    'state': {0: 'UP', 1: 'DOWN', 2: 'HOLD'}[event.keystate],
    'captured_at': datetime.datetime.fromtimestamp(event.event.timestamp()).isoformat()
  }

def is_to_be_logged(payload, config):
  filters = config.get('event_filters', None)
  if not filters: return True
  state_filters = filters.get('states', [])
  return payload['state'] in state_filters

def timestamp_s():
  return '[' + str(datetime.datetime.now()) + ']'

def output_line(string):
  print(timestamp_s() + ' ' + str(string))

if __name__ == '__main__':
  main()
