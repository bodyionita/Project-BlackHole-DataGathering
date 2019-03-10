from blackhole_data_gathering.util import read_from_json_file

from pymongo import MongoClient
import os

DIR = 'data/'


class DataPusher:

    def __init__(self):
        self.PRIMARY_CONNECTION_STRING =\
            'mongodb://project-blackhole:ZfgBV0pIae2rPmKKfX5k9VpUteQwcL3R5TcGCW2WAKvaynmkJRQPkGmJzKM6qI7pIGh9UEqU8' \
            'jout4UylbWr1A==@project-blackhole.documents.azure.com:10255/?ssl=true&replicaSet=globaldb'

        mongo_client = MongoClient(self.PRIMARY_CONNECTION_STRING)
        self.db = mongo_client.get_database('blackhole_data')
        self.details_collection = self.db.get_collection('symbols_details')

    def push_data(self):
        path = DIR + 'symbol_data/'

        symbols = read_from_json_file('symbols_extended')
        available_symbols = []
        for s in symbols:
            if not os.path.exists(path + s['symbol'] + '.json'):
                print('Symbol %s data not found.' % s['symbol'])
            else:
                self.push_symbol(s)
                available_symbols.append(s['symbol'])
        # TODO

    def push_symbol(self, symbol):
        if self.details_collection.find_one({'symbol': symbol}):
            print('Symbol %s already written to database' % symbol)
        else:
            self.details_collection.insert_one(symbol)

    def push_historical(self):
        raise NotImplementedError


