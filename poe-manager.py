#!/usr/bin/env python3

import math
import argparse
import requests
from random import random
from time import sleep, time


def main(args):
    print("Args:", args)

    s = requests.Session()
    url = "http://{}/cgi-bin/dispatcher.cgi".format(args.host)

    login_data = {
        "login": 1,
        "username": args.user,
        "password": encode(args.pwd),
        "dummy": current_time()
    }
    login_check_data = {
        "login_chk": 1,
        "dummy": current_time( )
    }

    print("Logging in...")
    s.get(url, params=login_data)
    sleep(1) # implicitely wait for login to occur
    ret2 = s.get(url, params=login_check_data)
    if not 'OK' in ret2.text:
        raise Exception("Login failed: %s" % ret2.text)

    print("Login successful, parsing cookie.")
    cookie = parse_cookie(s.get(url, params={"cmd": 1}))
    print("Got COOKIE: %s" % cookie)
    s.cookies.set("XSSID", cookie)

    print("Executing command: Turn %s PoE Port %s." % ('on' if args.state else 'off', args.port))
    command_data = {
        "XSSID": cookie,
        "portlist": args.port,
        "state": args.state,
        "portPriority": 2,
        "portPowerMode": 3,
        "portRangeDetection": 0,
        "portLimitMode": 0,
        "poeTimeRange": 20,
        "cmd": 775,
        "sysSubmit": "Apply"
    }
    ret = s.post(url, data=command_data)
    if 'window.location.replace' in ret.text:
        print("Command executed successfully!")
    else:
        raise Exception("Failed to execute command: %s" % ret.text)


def current_time():
    return int(time() * 1000.0)


def encode(_input):
    # The python representation of the JS function with the same name.
    # This could be improved further, but I can't be bothered.
    password = ""
    possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    _len = lenn = len(_input)
    i = 1
    while i <= (320-_len):
        if (0 == i % 7 and _len > 0):
            _len -= 1
            password += _input[_len]
        elif (i == 123):
          if (lenn < 10):
            password += "0"
          else:
            password += str(math.floor(lenn/10))
        elif (i == 289):
          password += str(lenn % 10)
        else:
          password += possible[math.floor(random() * len(possible))]
        i += 1
    return password


def parse_cookie(cmd_1):
    for line in cmd_1.text.split("\n"):
        if 'XSSID' in line:
            return line.replace('setCookie("XSSID", "', '').replace('");', '').strip()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Manage PoE ports for a Zyxel GS1900-10HP switch.')
    parser.add_argument('--host', '-H', dest='host', required=True, help='The hostname of the switch.')
    parser.add_argument('--user', '-U', dest='user', required=True, help='An administrative user.')
    parser.add_argument('--password', '-P', dest='pwd', required=True, help='Password of the admin user.')
    parser.add_argument('--port', '-p', dest='port', type=int, required=True, help='The port number.')
    parser.add_argument('--state', '-s', dest='state', type=int, choices=[0,1], required=True, help='Turn the port on (1) or off (0).')
    main(parser.parse_args())
