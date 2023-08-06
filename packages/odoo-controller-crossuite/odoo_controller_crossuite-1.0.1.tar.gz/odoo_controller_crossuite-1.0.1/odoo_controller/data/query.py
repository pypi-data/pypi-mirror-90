# data/query.py

import logging
logger = logging.getLogger(__name__)

class Query:

    def __init__(self, model):
        ''' constructor '''
        # set up class logger
        self.logger = logging.getLogger('{}.Query'.format(__name__))

        self.search_params = []
        self.modifiers = {}
        self.model = model

    def add_and(self, field, operator, value):
        ''' method to add search parameter evaluated as "AND" '''
        self.search_params.append((field, operator, value))
        return self

    def add_and_list(self, *args):
        ''' method to add search parameter(s) evaluated as "AND" '''
        for item in args:
            self.search_params.append(item)
        return self

    def add_or_list(self, *args):
        ''' method to add search parameter(s) evaluated as "OR" '''
        for i in range(len(args)-1):
            self.search_params.append('|')
        for item in args:
            self.search_params.append(item)
        return self

    def filter(self, fields):
        ''' method to select fields that should be returned '''
        self.modifiers['fields'] = fields
        return self

    def limit(self, limit):
        ''' method to limit results that should be returned '''
        self.modifiers['limit'] = limit
        return self

    def offset(self, offset):
        ''' method to set amount skipped results '''
        self.modifiers['offset'] = offset
        return self

    def sort(self, field, order='asc'):
        ''' method to sort results by field '''
        self.modifiers['order'] = '{} {}'.format(field, order)
        return self

    def __str__(self):
        ''' magic method to convert query object to string '''
        return 'MODEL:{} - SEARCH_PARAMS:{} - MODIFIERS:{}'.format(self.model, self.search_params, self.modifiers)
