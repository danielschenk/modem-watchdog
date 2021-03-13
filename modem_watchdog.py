#!/usr/bin/env python3

import argparse
import simpletr64
import requests
import time


def check_connection(attempts=3, timeout=2):
    for _ in range(attempts):
        try:
            requests.request('get', 'http://www.apple.com', timeout=timeout)
            return True
        except requests.exceptions.RequestException:
            pass
    return False


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--address',
                        help='hostname / IP address of the TR-064 device',
                        default='fritz.box')
    parser.add_argument('--tr64desc-port',
                        help='port of the web server serving the TR-064 description file on the device',
                        default=49000,
                        type=int)
    parser.add_argument('--tr64desc-path',
                        help='relative path to the TR-064 description file on the device',
                        default='tr64desc.xml')
    parser.add_argument('--username',
                        help='username for authentication',
                        default=None)
    parser.add_argument('--password',
                        help='password for authentication',
                        default=None)
    parser.add_argument('--check-interval',
                        default=20,
                        type=float)
    args = parser.parse_args()

    system = simpletr64.actions.System(args.address)
    if '://' not in args.address:
        args.address = 'http://' + args.address
    system.loadDeviceDefinitions(f'{args.address}:{args.tr64desc_port}/{args.tr64desc_path}')
    if args.username:
        system.username = args.username
    if args.password:
        system.password = args.password

    system.getTimeInfo()
    print('modem communication works')

    last_reboot_time = 0
    connected = False

    minimum = 5
    if args.check_interval < minimum:
        print(f'warning: raising check interval to {minimum}')
        args.check_interval = minimum
    
    while True:
        if check_connection():
            if not connected:
                connected = True
                print('internet connection detected')
        else:
            if connected:
                connected = False
                print('internet connection lost')

            if (now := time.time()) - last_reboot_time > 180:
                print('rebooting modem')
                try:
                    system.reboot()
                    last_reboot_time = now
                except requests.exceptions.RequestException as e:
                    print(f'failed to reboot modem: {e}')

        time.sleep(args.check_interval if connected else 1)


if __name__ == '__main__':
    main()
