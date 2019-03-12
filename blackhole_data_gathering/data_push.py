from blackhole_data_gathering.util import read_from_json_file
from blackhole_data_gathering.util import validate_number_of_years, get_start_end_date_tuple, date_range

from pymongo import MongoClient
import os

DIR = 'data/'
MINIMUM_COVERAGE = 68.89  # 68.86 - as found to be the max value found for more than half of the symbols
# on the time period 2014-01-14 to 2019-01-14
FAST_PUSH_ENABLED = True  # True to enable Fast Push.
"""
WARNING! 
Fast Push: - consumes a lot of memory  ~ 4GB of RAM 
           - runs fast                 ~ hours
Normal:    - consumes little memory    ~ 200MB of RAM 
           - runs slow                 ~ 10 hours 
"""

class DataPusher:

    def __init__(self, number_of_years=1):
        self.PRIMARY_CONNECTION_STRING =\
            'mongodb://project-blackhole:ZfgBV0pIae2rPmKKfX5k9VpUteQwcL3R5TcGCW2WAKvaynmkJRQPkGmJzKM6qI7pIGh9UEqU8' \
            'jout4UylbWr1A==@project-blackhole.documents.azure.com:10255/?ssl=true&replicaSet=globaldb'
        mongo_client = MongoClient(self.PRIMARY_CONNECTION_STRING)

        self.db = mongo_client.get_database('blackhole_data')
        self.details_collection = self.db.get_collection('symbols_details')
        self.historical_collection = self.db.get_collection('symbols_data')

        number_of_years = validate_number_of_years(number_of_years)
        self.date_tuple = get_start_end_date_tuple(number_of_years)

        self.available_symbols = []
        self.get_available_symbols()

        self.all_daily_data = {}  # WARNING! Will be used only if FAST_PUSH is enabled

    def get_available_symbols(self):
        path = DIR + 'symbol_data/'

        symbols = read_from_json_file(filename='symbols_extended')
        not_found = []
        for s in symbols:
            if not os.path.exists(path + s['symbol'] + '.json'):
                not_found.append(s['symbol'])
            else:
                self.available_symbols.append(s)
        print('Symbol data not found for following symbols(%s): %s' % (len(not_found), ', '.join(not_found)))
        print('Symbol data found for %s symbols' % (len(self.available_symbols)))

    def calculate_symbols_data_coverage(self):
        maximum = (self.date_tuple[1] - self.date_tuple[0]).days + 1
        for i, s in enumerate(self.available_symbols):
            symbol_data = read_from_json_file(filename=s['symbol'], subdir='symbol_data/')

            s['data_points'] = len(symbol_data)
            s['coverage'] = len(symbol_data) / maximum * 100
            self.available_symbols[i] = s

    def remove_symbols_with_low_data_coverage(self, min_coverage=68.0):
        removed = []

        for s in self.available_symbols:
            if s['coverage'] < min_coverage:
                removed.append(s['symbol'])
                self.available_symbols.remove(s)

        print('Symbols removed for not meeting the minimum coverage(%s) for the symbols(%s): %s'
              % (min_coverage, len(removed), ', '.join(removed)))

    def remove_symbols_no_data_for_start_date(self):
        removed = []
        date_string = self.date_tuple[0].strftime("%Y-%m-%d")

        for s in self.available_symbols:
            symbol_data = read_from_json_file(filename=s['symbol'], subdir='symbol_data/')
            if date_string not in symbol_data:
                removed.append(s['symbol'])
                self.available_symbols.remove(s)

        print('Symbols removed for not having data on start date(%s) for the symbols(%s): %s'
              % (date_string, len(removed), ', '.join(removed)))

    def push_data(self):
        self.calculate_symbols_data_coverage()
        self.remove_symbols_no_data_for_start_date()
        self.remove_symbols_with_low_data_coverage(68.89)
        print('Symbols left: %d' % len(self.available_symbols))

        #for s in self.available_symbols:
        #    self.push_symbol(s)

        self.push_historical()

    def push_symbol(self, symbol):
        if self.details_collection.find_one({'symbol': symbol['symbol']}):
            print('Symbol %s already written to database' % symbol['symbol'])
        else:
            self.details_collection.insert_one(symbol)

    def push_historical(self):
        if FAST_PUSH_ENABLED is False:  # NORMAL PUSH
            self.normal_push_historical()
        else:  # FAST PUSH
            self.fast_push_historical()

    def normal_push_historical(self):
        for date in date_range(self.date_tuple[0], self.date_tuple[1]):
            self.push_historical_day(date)

    def fast_push_historical(self):
        for date in date_range(self.date_tuple[0], self.date_tuple[1]):
            date_string = date.strftime("%Y-%m-%d")
            self.all_daily_data[date_string] = []

        for s in self.available_symbols:
            symbol_data = read_from_json_file(filename=s['symbol'], subdir='symbol_data/')
            for date in date_range(self.date_tuple[0], self.date_tuple[1]):
                date_string = date.strftime("%Y-%m-%d")
                data = {'name': s['symbol'], 'has_data': True, 'data': None}
                if date_string in symbol_data:
                    symbol_data_slice = symbol_data[date_string]
                    data['data'] = symbol_data_slice
                else:
                    data['has_data'] = False
                self.all_daily_data[date_string].append(data)

        for date in date_range(self.date_tuple[0], self.date_tuple[1]):
            date_string = date.strftime("%Y-%m-%d")
            new_date_document = {'date': date, 'symbols': self.all_daily_data[date_string]}

            if self.historical_collection.find_one({'date': date}):
                print('Data for %s already written to database' % date_string)
            else:
                print('Data for %s has been written to database' % date_string)
                self.historical_collection.insert_one(new_date_document)

    def push_historical_day(self, date):
        new_date_document = {'date': date, 'symbols': []}
        date_string = date.strftime("%Y-%m-%d")

        for s in self.available_symbols:
            symbol_data = read_from_json_file(filename=s['symbol'], subdir='symbol_data/')
            data = {'name': s['symbol'], 'has_data': True, 'data': None}
            if date_string in symbol_data:
                symbol_data_slice = symbol_data[date_string]
                data['data'] = symbol_data_slice
            else:
                data['has_data'] = False
            new_date_document['symbols'].append(data)

        if self.historical_collection.find_one({'date': date}):
            print('Data for %s already written to database' % date_string)
        else:
            print('Data for %s has been written to database' % date_string)
            self.historical_collection.insert_one(new_date_document)
