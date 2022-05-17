#!/usr/bin/python3

import argparse
from distutils.command.config import config
import random
import string
import logging

SUPPORTED_PLUGINS = []
services = []
routes = []
consumers = []

def name_it(size=6):
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(size))


def create_route(write_file, tag):
    name = name_it()
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
        strip_path: true
        tags: [{tag}]'''.format(name=name, tag=tag))
    routes.append(name)

def create_service(write_file, tag, num_routes=1):
    name = name_it()
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
      tags: [{tag}]
      routes:'''.format(name=name, tag=tag))
    services.append(name)
    for _ in range(num_routes):
        create_route(config_file, tag)
    logging.info('Added {num} routes for service {service}'.format(num=num_routes, service=name))

def create_consumer(write_file, tag):
    name = name_it()
    write_file.write('''
    - custom_id: {name}-id
      username: {name}
      tags: [{tag}]'''.format(name=name, tag=tag))
    consumers.append(name)

# def add_request_size_limiting_plugin(write_file, tag):


def get_args():
    parser = argparse.ArgumentParser(description='feed me your desired config')
    parser.add_argument('-o', '--outfile', default="kong.yaml", help="Name of file to write to.")
    parser.add_argument('-s', '--services', type=int, default=0, help="number of services you want (default is 0)")
    parser.add_argument('-r', '--routes', type=int, default=0, help="number of routes PER service (default is 0)")
    parser.add_argument('-c', '--consumers', type=int, default=0, help="number of consumers (default is 0)")
    parser.add_argument('-t', '--tag', default="test", help="tag to add to all entities (default is 'test')")
    parser.add_argument('-p', '--plugins', nargs='*', default=[], help="space-separated list of plugins to include. Supported plugins are: {plugins}".format(plugins=SUPPORTED_PLUGINS))
    parser.add_argument('-v', '--verbose', action='count', default=1, help="verbosity of output (leave off for quiet)" )

    args = parser.parse_args()
    return args

def setup_logs():
    # sets verbosity in python's logging module. -v = INFO, -vv = DEBUG
    # Thank you https://gist.github.com/ms5/9f6df9c42a5f5435be0e
    args.verbose = 40 - (10*args.verbose) if args.verbose > 0 else 0

    logging.basicConfig(level=args.verbose, format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

if __name__ == "__main__":
    args = get_args()

    setup_logs()

    with open(args.outfile, 'w') as config_file:
        config_file.write('_format_version: "2.1"')

        for i in range(args.services):
            if i == 0:
                config_file.write('\nservices:')
            create_service(config_file, args.tag, args.routes)
        logging.info('Added {} services'.format(args.services))
        logging.debug('Services list: {}'.format(services))
        logging.debug('Routes list: {}'.format(routes))

        for i in range(args.consumers):
            if i == 0:
                config_file.write('\nconsumers:')
            create_consumer(config_file, args.tag)
        logging.info('Added {} consumers'.format(args.consumers))
        logging.debug('Consumers list: {}'.format(consumers))


        for plugin in args.plugins:
            if plugin == "request-size-limiting":
                add_request_size_limiting_plugin(config_file, args.tag)
            else:
                logging.error('Plugin {plugin} not supported. Currently supported plugins are: {plugins}'.format(plugin=plugin, plugins=SUPPORTED_PLUGINS))