#!/usr/bin/env python3

__version__ = '0.2'

import argparse
import simpletr64
import requests
import time
import random
import logging


def check_connection(attempts=3, timeout=2):
    websites = [
        'http://www.apple.com',
        'http://www.github.com',
        'http://www.microsoft.com',
        'http://www.google.com',
        'http://www.python.org',
        'http://www.docker.com',
        'http://www.git-scm.com',
        'http://www.nrc.nl',
        'http://www.nist.gov',
    ]
    for _ in range(attempts):
        try:
            requests.request('get', random.choice(websites), timeout=timeout)
            return True
        except requests.exceptions.RequestException:
            pass
    return False


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--address',
                        help='hostname / IP address of the TR-064 device',
                        metavar='[HOST|IP]',
                        default='fritz.box')
    parser.add_argument('--port',
                        help='port of the TR-064 service on the device',
                        default=49000,
                        type=int)
    parser.add_argument('--tr64desc-path',
                        help='relative path to the TR-064 description file on the device',
                        metavar='PATH',
                        default='tr64desc.xml')
    parser.add_argument('--username',
                        help='username for authentication')
    parser.add_argument('--password',
                        help='password for authentication')
    parser.add_argument('--check-interval',
                        help='interval between internet connection checks, in seconds',
                        metavar='VALUE',
                        default=20,
                        type=float)
    parser.add_argument('--reboot-interval',
                        help='interval between repeated modem reboots during internet outage, in seconds',
                        metavar='VALUE',
                        default=600,
                        type=float)
    parser.add_argument('--logfile',
                        metavar='PATH',
                        help='log to specified file')
    parser.add_argument('-v', '--verbose',
                        help='verbose (enable debug messages on console)',
                        action='store_true')
    parser.add_argument('--version',
                        action='version',
                        version=f'%(prog)s {__version__}')
    args = parser.parse_args()

    logger = logging.getLogger('modem_watchdog')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if args.verbose else logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    if args.logfile:
        file_handler = logging.FileHandler(args.logfile)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.debug(f'logging to file {args.logfile}')
        logger.addHandler(file_handler)

    logger.info(f'started, version {__version__}')

    system = simpletr64.actions.System(args.address, port=args.port)
    if '://' not in args.address:
        args.address = 'http://' + args.address
    system.loadDeviceDefinitions(f'{args.address}:{args.port}/{args.tr64desc_path}')
    if args.username:
        system.username = args.username
    if args.password:
        system.password = args.password

    system.getTimeInfo()
    logger.info('TR-064 connection to modem succeeded')

    last_reboot_time = 0
    connected = False

    minimum = 5
    if args.check_interval < minimum:
        logger.warning(f'raising check interval to {minimum}')
        args.check_interval = minimum

    while True:
        if check_connection():
            if not connected:
                connected = True
                logger.info('internet connection detected')
        else:
            if connected:
                connected = False
                logger.info('internet connection lost')

            if (now := time.time()) - last_reboot_time > args.reboot_interval:
                logger.info('rebooting modem')
                try:
                    system.reboot()
                    last_reboot_time = now
                except requests.exceptions.RequestException as e:
                    logger.error(f'failed to reboot modem: {e}')
                except ValueError as e:
                    if 'could not execute' not in str(e).lower():
                        # not an exception of simpleTR64 as far as i know
                        raise
                    else:
                        logger.error(f'simpletr64: {e}')

        time.sleep(args.check_interval if connected else 1)


if __name__ == '__main__':
    main()
