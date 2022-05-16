#!/usr/bin/python3

import argparse
from distutils.command.config import config
import random
import string

def name_it(size=6):
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(size))

def create_route(write_file):
    write_file.write('''
      - https_redirect_status_code: 426
        name: {name}-route
        path_handling: v0
        paths:
        - /{name}
        preserve_host: false
        protocols:
        - http
        - https
        regex_priority: 0
        request_buffering: true
        response_buffering: true
        strip_path: true'''.format(name=name_it()))

def create_service(write_file, num_routes=1):
    write_file.write('''
    - connect_timeout: 60000
      host: httpbin.org
      name: {name}-service
      path: /anything/{name}
      port: 80
      protocol: http
      read_timeout: 60000
      write_timeout: 60000
      retries: 5
      routes:'''.format(name=name_it()))
    for _ in range(num_routes):
        create_route(config_file)

def create_consumer(write_file):
    write_file.write('''
    - custom_id: {name}-id
      username: {name}'''.format(name=name_it()))


parser = argparse.ArgumentParser(description='feed me your desired config')
# parser.add_argument('-w', '--workspaces', type=int, choices=range(1, 100), default=1, help="number of workspaces to add [1-3, default is 1]")
parser.add_argument('-o', '--outfile', default="kong.yaml", help="Name of file to write to.")
parser.add_argument('-s', '--services', type=int, default=1, help="number of services you want [1-100, default 1])")
parser.add_argument('-r', '--routes', type=int, default=1, help="number of routes PER service [1-100, default 1]")
parser.add_argument('-c', '--consumers', type=int, default=0, help="number of consumers [1-100, default 0]")
# parser.add_argument('-t', '--tag', help="tag to add to all entities")
# parser.add_argument('-u', '--add-upstream', action="store_true", help="add preset upstream to config (default ws only)")
# parser.add_argument('-p', '--plugins', nargs='*', help="space-separated list of plugins to include. Supported plugins are: [TBD]")
# parser.add_argument('-a', '--admins', type=int, choices=range(1, 5), help="number of admins to add per workspace [1-5, default is 1]")
# parser.add_argument('-r', '--rbac-users', type=int, choices=range(1, 10), help="number of RBAC users to add per workspace [1-10, default 0]")

args = parser.parse_args()

if args.services > 1000 or args.routes > 1000:
    print("Please respect my rules! 100 or less, route or service.")
    exit(1)

with open(args.outfile, 'w') as config_file:
    config_file.write('_format_version: "1.1"')

    for i in range(args.services):
        if i == 0:
            config_file.write('\nservices:')
        create_service(config_file, args.routes)

    for i in range(args.consumers):
        if i == 0:
            config_file.write('\nconsumers:')
        create_consumer(config_file)