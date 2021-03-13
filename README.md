modem-watchdog
==============
_A workaround for disappointing modems._

This script monitors an internet connection and tries to reboot a TR064-compatible modem
(like a FRITZ!Box) if the internet connection seems broken. It was inspired by some issues with my modem and ISP.
I noticed that my FRITZ!Box is not always able to recover by itself after a DSL line failure, but mostly will after a
reboot.

The script is configurable, execute `modem_watchdog.py --help` for available options.

Thanks to [bpannier](https://github.com/bpannier) for making the
[simpleTR64 library](https://github.com/bpannier/simpletr64) used in this project.

## Running the script in a Docker container
No builds of this Docker image are published (yet). However, it is very easy to build it locally,
or even better, have docker-compose do that for you.

### With docker-compose
Add a service like this to your `docker-compose.yml`:
```yml
  modem-watchdog:
    container_name: modem-watchdog
    build: https://github.com/danielschenk/modem-watchdog.git
    restart: always
    environment:
      TZ: "Europe/Amsterdam" # change as needed, will ensure logging in local time
    entrypoint:
      - "./modem_watchdog.py"
      - "--address"
      - "192.168.1.1"
      - "--user"
      - "foo"
      - "--password"
      - "bar"
```

### Without docker-compose
1. `docker build -t modem-watchdog https://github.com/danielschenk/modem-watchdog.git`
2. `docker run -d modem-watchdog ./modem_watchdog.py --address 192.168.1.1 --username foo --password bar`

## Running the script directly
Requirements:
- Python 3.8.x
- Some required packages, can be installed with: `pip3 install -r requirements.txt`
