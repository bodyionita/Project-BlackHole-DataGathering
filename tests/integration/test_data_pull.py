from blackhole_data_gathering.data_pull import DataPuller
from blackhole_data_gathering.util import read_from_json_file
from threading import Lock

import unittest
import shutil
from datetime import datetime


class TestDataPull(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.data_puller = DataPuller()
        self.data_dir = 'data/'
        self.subdir = 'test/'
        self.dir = self.data_dir + self.subdir
        self.lock = Lock()
        self.lock.acquire()

    @classmethod
    def tearDownClass(self):
        self.lock.acquire()
        shutil.rmtree(self.dir)

        infile = open(self.data_dir + 'symbols_not_found.txt', 'r')
        lines = infile.read().splitlines()
        infile.close()

        with open(self.data_dir + 'symbols_not_found.txt', 'w') as outfile:
            for line in lines[:-1]:
                outfile.write(str(line) + '\n')
        self.lock.release()

    def test_1_pull_symbols(self):
        filename = 'test_symbols'
        self.data_puller.pull_symbols(filename=filename, subdir=self.subdir)
        symbols = read_from_json_file(filename=filename, subdir=self.subdir)

        self.assertEqual(symbols[0]['symbol'], 'A')

    def test_2_pull_symbols_extended(self):
        filename = 'test_symbols_extended'
        symbols = [{
                    "symbol": "A",
                    "name": "Agilent Technologies Inc.",
                    "date": "2019-01-14",
                    "isEnabled": True,
                    "type": "cs",
                    "iexId": "2"
                  }]
        data_verify = [{
                        "symbol": "A",
                        "companyName": "Agilent Technologies Inc.",
                        "exchange": "New York Stock Exchange",
                        "industry": "Medical Diagnostics & Research",
                        "website": "http://www.agilent.com",
                        "description": "Agilent Technologies Inc is engaged in life sciences, diagnostics and" +
                                       " applied chemical markets. The company provides application focused " +
                                       "solutions that include instruments, software, services and consumables" +
                                       " for the entire laboratory workflow.",
                        "CEO": "Michael R. McMullen",
                        "issueType": "cs",
                        "sector": "Healthcare",
                        "tags": [
                          "Healthcare",
                          "Diagnostics & Research",
                          "Medical Diagnostics & Research"
                        ]
                      }]

        self.data_puller.pull_symbols_extended(symbols=symbols, filename=filename, subdir=self.subdir)
        data = read_from_json_file(filename=filename, subdir=self.subdir)

        self.assertEqual(data_verify, data)

    def test_3_pull_historical_data(self):
        symbols = ['A']
        date = datetime(2019, 1, 14)

        data_verify = {
                        "2019-01-14": {
                            "open": 69.5778,
                            "high": 70.1466,
                            "low": 69.5279,
                            "close": 69.6077,
                            "volume": 2182673
                        }
                      }

        self.data_puller.pull_historical(symbols=symbols, date=(date, date), subdir=self.subdir)
        data = read_from_json_file(filename=symbols[0], subdir=self.subdir)

        self.assertEqual(data_verify, data)

    def test_4_pull_historical_data_wrong_symbol(self):
        symbols = ['A_WRONG_SYMBOL']
        date = datetime(2019, 1, 14)

        try:
            self.data_puller.pull_historical(symbols=symbols, date=(date, date), subdir=self.subdir)
        finally:
            with open(self.data_dir + 'symbols_not_found.txt', 'r') as infile:
                lines = infile.read().splitlines()
                self.lock.release()
                self.assertEqual(lines[-1],
                                 'Symbol A_WRONG_SYMBOL not found.')


if __name__ == '__main__':
    unittest.main()
