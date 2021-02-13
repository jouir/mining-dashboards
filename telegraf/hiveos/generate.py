#!/usr/bin/env python3
import requests
import os
import sys
import logging
import argparse

from jinja2 import Environment, FileSystemLoader

logger = logging.getLogger(__name__)

RETURN_OK=0
RETURN_ERROR=1


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', dest='loglevel', action='store_const', const=logging.INFO,
                        help='print more output')
    parser.add_argument('-d', '--debug', dest='loglevel', action='store_const', const=logging.DEBUG,
                        default=logging.WARNING, help='print even more output')
    args = parser.parse_args()
    return args


def setup_logging(args):
    log_format = '%(levelname)s: %(message)s'
    logging.basicConfig(format=log_format, level=args.loglevel)


class HiveAPI:
    def __init__(self, token):
        session = requests.Session()
        session.headers.update({'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'})
        self.session = session
        self.base_url = 'https://api2.hiveos.farm/api/v2'
        self.farms = {}
        for farm in self.fetch_farms():
            self.farms[farm] = self.fetch_workers(farm_id=farm.number)

    def fetch_farms(self):
        r = self.session.get(f'{self.base_url}/farms')
        r.raise_for_status()
        farms = r.json().get('data')
        if farms:
            return [Farm(number=f['id'], name=f['name']) for f in farms]

    def fetch_workers(self, farm_id):
        r = self.session.get(f'{self.base_url}/farms/{farm_id}/workers')
        r.raise_for_status()
        workers = r.json().get('data')
        if workers:
            return [Worker(number=w['id'], farm_id=farm_id, name=w['name']) for w in workers]


class Farm:
    def __init__(self, number, name):
        self.number = number
        self.name = name

    def __repr__(self):
        return f'<Farm #{self.number}({self.name})>'


class Worker:
    def __init__(self, number, farm_id, name):
        self.number = number
        self.farm_id = farm_id
        self.name = name

    def __repr__(self):
        return f'<Worker #{self.number}({self.name}@Farm#{self.farm_id})>'


def create_farm_configuration(farm_id):
    template_variables = {'farm_id': farm_id}
    return create_configuration(template_name='farm.conf.j2', template_variables=template_variables)


def create_worker_configuration(farm_id, farm_name, worker_id, worker_name):
    template_variables = {'farm_id': farm_id, 'farm_name': farm_name, 'worker_id': worker_id,
                          'worker_name': worker_name}
    return create_configuration(template_name='worker.conf.j2', template_variables=template_variables)


def create_configuration(template_name, template_variables):
    template_path = os.path.split(os.path.abspath(__file__))[0]
    loader = FileSystemLoader(template_path)
    env = Environment(loader=loader)
    template = env.get_template(template_name)
    text = template.render(**template_variables)
    return text


def main():
    args = parse_arguments()
    setup_logging(args)

    token = os.getenv('HIVEOS_TOKEN')
    if not token:
        logger.error('Missing HIVEOS_TOKEN environment variable')
        return RETURN_ERROR

    logger.info('crawling HiveOS API')
    api = HiveAPI(token=token)

    configurations = []
    for farm in api.farms:
        logger.info(f"generating configuration for farm {farm}")
        configurations.append(create_farm_configuration(farm_id=farm.number))
        for worker in api.farms[farm]:
            logger.info(f'generating configuration for worker {worker}')
            configurations.append(create_worker_configuration(farm_id=farm.number, farm_name=farm.name,
                                                              worker_id=worker.number, worker_name=worker.name))

    logger.info('writing configuration to file')
    with open('hiveos.conf', 'w') as fd:
        fd.write('\n'.join(configurations))

    return RETURN_OK


if __name__ == '__main__':
    sys.exit(main())
