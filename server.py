import evdev

DEVICE_PATH = '/dev/input/event0'

dev = evdev.InputDevice(DEVICE_PATH)
print('Capturing device: ' + str(dev))

for event in dev.read_loop():
  if event.type == evdev.ecodes.EV_KEY:
    print(evdev.categorize(event))
