# Android VR - BlackHole - Data Gathering [![Build Status](https://travis-ci.com/bodyionita/Project-BlackHole-DataGathering.svg?branch=master)](https://travis-ci.com/bodyionita/Project-BlackHole-DataGathering) [![codecov](https://codecov.io/gh/bodyionita/Project-BlackHole-DataGathering/branch/master/graph/badge.svg)](https://codecov.io/gh/bodyionita/Project-BlackHole-DataGathering)

*This is part of an industry project on which my dissertation is based on. The paper can be found [here](https://drive.google.com/file/d/17fM2qNF6F9nBIIymw9ciUfRFP3HBxboI/view?usp=sharing).
The main project repo is [Project BlackHole](https://github.com/bodyionita/Project-BlackHole).
The project development ran from :calendar: __09/2018__ to __04/2019__. :calendar:*

## About :information_source:

A python file used for pulling stock market data from [IEX's API](https://iextrading.com/developer/) using the
[IEX Finance](https://pypi.org/project/iexfinance/) python module and pushing the data to 
[Microsoft Azure's](https://azure.microsoft.com/en-us/) Cosmos DocumentDB.

## Getting Started
1. Get python 3.5 x64 bit version
2. Get git
3. Clone this repository by `git clone https://github.com/bodyionita/Project-BlackHole-DataGathering.git`
4. Change to the root directory of it `cd Project-BlackHole-DataGathering`
5. Run in terminal `pip install -U pip`
6. Run in terminal `python setup.py install` to install the requirements
8. Configure the module according to your needs as explained bellow
7. Create an Azure CosmosDB DocumentDB database
8. Run the module in terminal by `python blackhole_data_gatherer/data_orchestrator.py`
9. It may take up to 15 hours to complete based on your configurations

## Configurations
1. Navigate to the `blackhole_data_gatherer/data_push.py` and set the `FAST_PUSH_ENABLED` at the top according to your needs
2. Navigate to the `blackhole_data_gatherer/data_push.py` and set the `MINIMUM_COVERAGE` at the top according to your needs
3. Navigate to the `blackhole_data_gatherer/data_push.py` and set the `PRIMARY_CONNECTION_STRING` at line 23 to the connection string you get from the CosmosDB interface
4. Navigate to the `blackhole_data_gatherer/data_orchestrator.py`, in the `main` function,  `orchestrator = DataOrchestrator(5)`. Change the 5 to the number of years of data you want to download

## Testing
To test the package run `coverage run -m unittest discover -s tests/ -v` from the root directory

## Contributors :pencil2:

- **[Bogdan Ionita](https://www.linkedin.com/in/bionita/)** - Author 

    I am a 4th year Computer Science student at [University College London](https://www.ucl.ac.uk/) 
    and have chosen to do this industry project as basis for my dissertation.

    :e-mail:  bogdan.ionita96@gmail.com

    :e-mail:  bogdan.ionita.15@ucl.ac.uk

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE)
file for details
