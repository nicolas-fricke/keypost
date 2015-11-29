# KeyPost

Simple service which listens to events of a device in `/dev/input/` and posts them to a user-defined URL.
With this service you can turn regular input devices, such as computer mice or keyboards into switches for the Internet of Things.

# Setup

1. Make sure that you have a running version of Python 2 and `pip` installed
1. Clone this repository
1. Within it, run `pip install -r requirements.txt` to install all dependencies
1. Then copy the file `config.yml.default` and rename it to `config.yml`
1. Open it and change the `device_path` to the device you want to monitor and `post_url` to the URL where the `POST`-requests should be sent to. Read more about the `post_url` and its payload in the following section.
1. Now you should be ready to go! Run `python server.py` to start the server

# POST URL and payload

KeyPost is sending an individual POST request for every captured input event.
The URL these POST requests are sent to is set within `config.yml` as `post_url`.
This URL may contain any key from the payload as a (Python formatted) placeholder, see examples below.

The payload is JSON and contains the following information:
```js
{
  "key": "BTN_LEFT", // human readable unique identifier of the pressed key / button, this is coming from the library `evdev` (https://www.kernel.org/doc/Documentation/input/event-codes.txt)
  "code": 272, // the key code of the pressed button / key
  "state": "DOWN", // either "DOWN", "UP", or "HOLD". You can configure which of these are being tracked within `config.yml`
  "created_at": "2015-11-29T02:19:44.412690" // timestamp in ISO 8601 format with milliseconds when the event was captured
}
```

Therefore, a valid URL in the config with placeholders can look like the following:
```
post_url: http://my_server.example.com/key_events/%(key)s/%(state)s
```
which would for the above payload issue a request to:
```
http://my_server.example.com/key_events/BTN_LEFT/DOWN
```

In any case, the full payload will be sent.

# Use Case: IFTTT Maker

You probably know [IFTTT](https://ifttt.com), a web service to connect different online APIs and trigger actions based on events.
I implemented KeyPost specifically to play nicely with [IFTTT's Maker channel](https://ifttt.com/maker).
The idea is to use a Raspberry Pi with a connected mouse (better even: a wireless mouse) to trigger whatever action is desired – from switching lights to posting a pre-set status update on Twitter.
Cheap buttons for the IoT - here we come!

This is how you can wire KeyPost and the Maker channel together:

1. Install KeyPost on your local server, as described under _Setup_
1. Go to https://ifttt.com/maker and, if not already done, connect the channel to your account
1. In the `config.yml` set the `post_url` to: `https://maker.ifttt.com/trigger/%(key)s_%(state)s/with/key/<your-maker-key>` where you have to replace `<your-maker-key>` with your personal key you find on the maker page
1. Create a new recipe where you select _Maker_ as the trigger channel (_if_ part)
1. You are then prompted to enter an _Event Name_, enter something in the format of `<key>_<state>`, e.g. `BTN_LEFT_DOWN`
1. Choose whatever you want for the _then_ part of your recipe
1. Start the server on your device and try what happens if you press the set button

# Contributing

Please do! It's easy as 1-2-3 (okay, and 4-5 ;) )

1. Fork it (https://github.com/nicolas-fricke/keypost/fork)
1. Create your feature branch (`git checkout -b my-new-feature`)
1. Commit your changes (`git add my_file.py` and `git commit -m 'Add some feature'`)
1. Push to the branch (`git push origin my-new-feature`)
1. Create a new Pull Request, describe what and why you added the changes
