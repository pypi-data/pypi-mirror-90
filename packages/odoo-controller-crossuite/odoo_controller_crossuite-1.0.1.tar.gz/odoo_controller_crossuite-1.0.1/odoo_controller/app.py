# app.py

import logging
logger = logging.getLogger(__name__)

import pathlib
import os
import yaml
import pprint
import calendar
import datetime
from odoo_controller.data.controller import Controller
from odoo_controller.data.query import Query

def humanize_time(secs):
    mins, secs = divmod(secs, 60)
    hours, mins = divmod(mins, 60)
    return "{:.0f}:{:.0f}:{:.0f}".format(hours, mins, secs)


def run():
    logger.info('App running')
    # Create a controller from config file
    cur_path = pathlib.Path(__file__).parent.parent.absolute()
        
    if os.environ['ENV'] == 'development':
        db = Controller().from_config_connected('{}/config/odoo_credentials.dev.yaml'.format(cur_path))
    else:
        db = Controller().from_config_connected('{}/config/odoo_credentials.yaml'.format(cur_path))
    

if __name__ == '__main__':
    run()