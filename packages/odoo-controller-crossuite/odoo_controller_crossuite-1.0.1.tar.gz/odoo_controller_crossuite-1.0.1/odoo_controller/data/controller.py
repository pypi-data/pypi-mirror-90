# data/controller.py

import logging
logger = logging.getLogger(__name__)

# TODO: add logger for database logging
# TODO: add documentation sphinx

import pprint
import xmlrpc.client
import yaml
from .query import Query

class Controller:
    
    def __init__(self):
        ''' constructor '''
        # set up class logger
        self.logger = logging.getLogger('{}.Controller'.format(__name__))

        # credentials of the server and database
        self.server_credentials = {
            'url': '',
            'db': '',
            'timezone': ''
        }
        # credentials of the user
        self.user_credentials = {
            'username': '',
            'password': ''
        }
        # protected authentication variables
        self._common = None
        self._db = None
        self._uid = None

        self.logger.debug('Created new instance of Controller')

    @classmethod
    def from_config(cls, file):
        ''' alternative constructor from yaml config file (not-connected instance) '''
        with open(file) as f:
            config = yaml.safe_load(f)
        controller = cls()
        controller.configure_server(config['server']['url'], config['server']['db'])
        controller.configure_user(config['user']['username'], config['user']['password'])
        return controller

    @classmethod
    def from_config_connected(cls, file):
        ''' alternative constructor from yaml config file (connected instance) '''
        with open(file) as f:
            config = yaml.safe_load(f)
        controller = cls()
        controller.configure_server(config['server']['url'], config['server']['db'])
        controller.configure_user(config['user']['username'], config['user']['password'])
        controller.connect()
        return controller

    def configure_server(self, url, db, timezone="UTC"):
        ''' method to configure the server credentials '''
        self.server_credentials['url'] = url
        self.server_credentials['db'] = db
        self.server_credentials['timezone'] = timezone

        self.logger.info('Server configured')

    def configure_user(self, username, password):
        ''' method to configure the user credentials '''
        self.user_credentials['username'] = username
        self.user_credentials['password'] = password

        self.logger.info('User configured')

    def connect(self):
        ''' method to connect and authenticate to the database '''
        try:
            self._common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(self.server_credentials['url']))
            self._uid = self._common.authenticate(self.server_credentials['db'], self.user_credentials['username'], self.user_credentials['password'], {})
            self._db = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.server_credentials['url']))
            self._db.execute_kw(self.server_credentials['db'], self._uid, self.user_credentials['password'],
                                'res.users', 'check_access_rights', ['read'], {'raise_exception': False})
        # TODO: add error handling for connect() method
        except xmlrpc.client.ProtocolError as e:
            self.logger.exception(e)
            raise e
        except Exception as e:
            self.logger.exception(e)
            raise(e)
        else:
            self.logger.info('Connected and authenticated on server')
    
    def search_by_id(self, model, id):
        ''' method to search by id '''
        self.logger.info('Running search on model {} by id: {}'.format(model, id))
        try:
            return self._db.execute_kw(self.server_credentials['db'], self._uid, self.user_credentials['password'],
                                        model, 'search', [[('id', '=', id)]])[0]
        except IndexError as e:
            # no results were found
            return None

    def search_read_by_id(self, model, id, fields=[]):
        ''' method to search_read by id '''
        self.logger.info('Running search_read on model {} by id: {}'.format(model, id))
        try:
            return self._db.execute_kw(self.server_credentials['db'], self._uid, self.user_credentials['password'],
                                        model, 'search_read', [[('id', '=', id)]], {'fields': fields})[0]
        except IndexError as e:
            # no results were found
            return None
    
    def search_by_query(self, query):
        ''' method to search by query '''
        self.logger.info('search by query: {}'.format(query))
        return self._db.execute_kw(self.server_credentials['db'], self._uid, self.user_credentials['password'],
                                        query.model, 'search', [query.search_params], query.modifiers)

    def search_read_by_query(self, query):
        ''' method to search_read by query '''
        self.logger.info('search_read by query: {}'.format(query))
        return self._db.execute_kw(self.server_credentials['db'], self._uid, self.user_credentials['password'],
                                        query.model, 'search_read', [query.search_params], query.modifiers)

    def count_by_query(self, query):
        ''' method to count results from query '''
        self.logger.info('Count by query: {}'.format(query))
        return self._db.execute_kw(self.server_credentials['db'], self._uid, self.user_credentials['password'],
                                        query.model, 'search_count', [query.search_params])
    
    @staticmethod
    def format_results(results, indentation=2):
        ''' method to format results in pretty string '''
        return pprint.pformat(results, indentation)






