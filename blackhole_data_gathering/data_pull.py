from iexfinance.refdata import get_symbols
from iexfinance.stocks import get_historical_data, Stock
from iexfinance.utils.exceptions import IEXSymbolError

from blackhole_data_gathering.util import write_to_json_file
from datetime import datetime


class DataPuller:

    @staticmethod
    def pull_symbols(filename='symbols', subdir=''):
        """
        Gets all the stock symbols with the following keys and writes it to a file in the data folder.

        symbol	    refers to the symbol represented in Nasdaq Integrated symbology (INET).
        name	    refers to the name of the company or security.
        date	    refers to the date the symbol reference data was generated.
        isEnabled	will be true if the symbol is enabled for trading on IEX.
        type	    refers to the common issue type
        iexId	    unique ID applied by IEX to track securities through symbol changes.

        :param filename: string -> name of the file the data should be written to
        :param subdir: string -> subdirectory name followed by /
        """

        symbols = get_symbols()

        write_to_json_file(data=symbols, filename=filename, subdir=subdir)

    @staticmethod
    def pull_symbols_extended(symbols, filename='symbols_extended', subdir='symbol_data'):
        """
        Gets all the stock symbols with the following keys and writes it to a file in the data folder
        and differs from the simple symbols method as it contains a bit more data

        symbol	    refers to the symbol represented in Nasdaq Integrated symbology (INET).
        companyName	refers to the name of the company or security.
        exchange	the stock exchange in which the symbol is traded
        industry	the industry in which the company operates
        website     the website of the company
        description	the description of the company
        CEO	        name of the CEO of the company
        issueType	refers to the common issue type of the stock.
                    ad – American Depository Receipt (ADR’s)
                    re – Real Estate Investment Trust (REIT’s)
                    ce – Closed end fund (Stock and Bond Fund)
                    si – Secondary Issue
                    lp – Limited Partnerships
                    cs – Common Stock
                    et – Exchange Traded Fund (ETF)
                    (blank) = Not Available, i.e., Warrant, Note, or (non-filing) Closed Ended Funds
        sector	    the sector in which the company operates
        tags	    an array of strings used to classify the company.

        :param symbols: [string] -> list of all the symbols to get data for
        :param filename: string -> name of the file the data should be written to
        :param subdir: string -> subdirectory name followed by /
        """
        symbols_extended = []
        for symbol in symbols:
            stock = Stock(symbol['symbol'], output_format='json')
            symbol_extended = stock.get_company()
            symbols_extended.append(symbol_extended)

        write_to_json_file(data=symbols_extended, filename=filename, subdir=subdir)

    @staticmethod
    def pull_historical(symbols, date_start=None, date_end=None, subdir='symbol_data/'):
        """
        Gets historical data with a granularity of 1 day for a list of symbols and writes them into separate JSON
        files into the data folder with the following keys

        date    the date for which the data is present
        open    the open price of the stock
        high    the highest price the stock reached
        low     the lowest price the stock reached
        close   the closing price of the stock
        volume  the volume transacted

        :param symbols: [string] -> list of all the symbols to get data for
        :param date_start: datetime -> start date of the historical data
        :param date_end: datetime -> end date of the historical data
        :param subdir: string -> subdirectory name followed by /
        """
        if (date_start is None) and (date_end is None):
            date_end = datetime.today()
            date_start = datetime(date_end.year - 1, date_end.month, date_end.day)

        for symbol in symbols:
            try:
                symbol_data = get_historical_data(symbol, date_start, date_end, output_format='json')
            except IEXSymbolError as e:
                with open('data/symbols_not_found.txt', 'a') as outfile:
                    outfile.write(str(e)+'\n')
            else:
                write_to_json_file(data=symbol_data, filename=symbol, subdir=subdir)
