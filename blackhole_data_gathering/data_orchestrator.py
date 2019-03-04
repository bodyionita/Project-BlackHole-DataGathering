from blackhole_data_gathering.data_pull import DataPuller
from blackhole_data_gathering.util import read_from_json_file
from datetime import datetime


class DataOrchestrator:
    """
    Orchestrator of the data pulling from the API and pushing into the Azure with a default range of up to 5 years.

    """

    def __init__(self, no_years=5):
        if no_years > 5:
            self.number_of_years = 5
        else:
            self.number_of_years = no_years

    def pull_and_write_data(self):
        """
        Pull all the data to be worked with and writes it into the data folder
        """
        # Pull all symbols from API and write to json file
        DataPuller.pull_symbols()

        # Read all symbols' data from the json file
        symbols_data = read_from_json_file('symbols')

        # Aggregate into array only symbols
        symbols = []
        for symbol_data in symbols_data:
            symbols.append(symbol_data['symbol'])

        # Pull extended symbols data from API and write to json file
        DataPuller.pull_symbols_extended(symbols)

        # Set start and end date for the historical data
        end_date = datetime.today()
        start_date = datetime(end_date.year - self.number_of_years, end_date.month, end_date.day)

        # One by one, get historical data for each of the symbols and write into a separate file
        DataPuller.pull_historical(symbols, start_date, end_date)

    def read_and_push_data(self):
        """
        Read all the data to be worked with from the data folder and push it to Azure
        """


def main():

    orchestrator = DataOrchestrator()

    # orchestrator.pull_and_write_data()
    orchestrator.read_and_push_data()


if __name__ == '__main__':
    main()
