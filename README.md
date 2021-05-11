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
Docker images are available for some common platforms. Alternatively, the image can be built locally.

### With docker-compose
Add a service like this to your `docker-compose.yml`:
```yml
  modem-watchdog:
    container_name: modem-watchdog
    image: danielschenk/modem-watchdog:0.2
    # alternative: build locally
    # build: https://github.com/danielschenk/modem-watchdog.git#v0.2.0
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

### Without docker-compose (pull image)
`docker run -d danielschenk/modem-watchdog:0.2 --address 192.168.1.1 --username foo --password bar`

### Without docker-compose (build image locally)
1. `docker build -t modem-watchdog https://github.com/danielschenk/modem-watchdog.git#v0.2.0`
2. `docker run -d modem-watchdog --address 192.168.1.1 --username foo --password bar`

## Running the script directly
Requirements:
- Python 3.8.x
- Some required packages, can be installed with: `pip3 install -r requirements.txt`
