# __main__.py

import logging
import logging.config
import pathlib

# configure logging for application
cur_path = pathlib.Path(__file__).parent.parent.absolute()
logging.config.fileConfig('{}/log/logging.conf'.format(cur_path))
logger = logging.getLogger(__name__)

from odoo_controller import app

if __name__ == '__main__':
    app.run()