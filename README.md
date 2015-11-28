# KeyPost

Simple service which listens to events of a device in `/dev/input/` and posts them to a user-defined URL.
With this service you can turn regular input devices, such as computer mice or keyboards into switches for the Internet of Things.

# Setup

1. Make sure that you have a running version of Python 2 and `pip` installed
1. Clone this repository
1. Within it, run `pip install -r requirements.txt` to install all dependencies
1. Then copy the file `config.yml.default` and rename it to `config.yml`
1. Open it and change the `device_path` to the device you want to monitor and `post_url` to the URL where the `POST`-requests should be sent to
1. Now you should be ready to go! Run `python server.py` to start the server


# Contributing

Please do! It's easy as 1-2-3 (okay, and 4-5 ;) )

1. Fork it (https://github.com/nicolas-fricke/keypost/fork)
1. Create your feature branch (`git checkout -b my-new-feature`)
1. Commit your changes (`git add my_file.py` and `git commit -m 'Add some feature'`)
1. Push to the branch (`git push origin my-new-feature`)
1. Create a new Pull Request, describe what and why you added the changes
