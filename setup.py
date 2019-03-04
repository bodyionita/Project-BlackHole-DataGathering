from setuptools import setup, find_packages

setup(
    name='blackhole_data_gathering',
    version='0.1.0',
    description='A module for pulling data from IEX API using iexfinance module and pushing it to Azure',
    url='https://github.com/bodyionita/Project-BlackHole-DataGathering/tree/master/',
    license='GNU General Public License v3.0',
    author='Bogdan Ionita',
    author_email='bogdan.ionita.15@ucl.ac.uk',
    packages=find_packages(),
    install_requires=['iexfinance', 'codecov', 'flake8'],
)
