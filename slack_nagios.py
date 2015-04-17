#!/bin/python

import argparse
import requests

"""
A simple script to post nagios notifications to slack

Similar to https://raw.github.com/tinyspeck/services-examples/master/nagios.pl
But adds proxy support

Note: If your internal proxy only exposes an http interface, you will need to be running a modern version of urllib3.
See https://github.com/kennethreitz/requests/issues/1359

Designed to work as such:
slack_nagios.py -field slack_channel=#alerts -field HOSTALIAS="$HOSTNAME$" -field SERVICEDESC="$SERVICEDESC$" -field SERVICESTATE="$SERVICESTATE$" -field SERVICEOUTPUT="$SERVICEOUTPUT$" -field NOTIFICATIONTYPE="$NOTIFICATIONTYPE$"
slack_nagios.py -field slack_channel=#alerts -field HOSTALIAS="$HOSTNAME$" -field HOSTSTATE="$HOSTSTATE$" -field HOSTOUTPUT="$HOSTOUTPUT$" -field NOTIFICATIONTYPE="$NOTIFICATIONTYPE$"
"""


def send_alert(args):
    if args.proxy:
        proxy = {
            "http": args.proxy,
            "https": args.proxy
        }
    else:
        proxy = {}

    url = "https://{d}/services/hooks/nagios?token={t}".format(
        d=args.domain,
        t=args.token
    )

    payload = {
        'slack_channel': "#" + args.channel
    }

    for field in args.field:
        key, value = field[0].split('=')
        payload[key] = value

    req = requests.post(url=url, proxies=proxy, data=payload)
    if args.debug:
        print(req.text)
        print(req.status_code)
    return req


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Post nagios notifications to slack")

    parser.add_argument('--debug', help="Debug mode", action='store_true')
    parser.add_argument('--proxy', '-p', help="Proxy to use, full url format", default=None)
    parser.add_argument('--domain', '-d', help="Slack domain to post to", required=True)
    parser.add_argument('--channel', '-c', help="Channel to post to", required=True)
    parser.add_argument('--token', '-t', help="Auth token", required=True)
    parser.add_argument('-field', nargs='*', required=True, action='append',
                        help="Alert fields (Should be specified more than once)")

    args = parser.parse_args()
    send_alert(args)
