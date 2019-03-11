import json
import os
from datetime import datetime

DIR = 'data/'


def write_to_json_file(data, filename, subdir=''):
    """
    Method which takes data to dump it into a JSON file in the data folder.

    :param data: [dict] or dict
    :param filename: string -> name of the file to be written to
    :param subdir: string -> subdirectory name for putting the file in. tailed with '/'
    """
    path = DIR + subdir
    mode = 'w'

    if not os.path.exists(path):
        os.makedirs(path)

    file_path = path + filename + '.json'
    try:
        with open(file_path, mode) as outfile:
            json.dump(data, outfile, indent=2, separators=(',', ': '))
    except OSError as e:
        with open('data/symbols_not_found.txt', 'a') as outfile:
            outfile.write(str(e) + '\n')
        raise e


def read_from_json_file(filename, subdir=''):
    """
    Method which reads a JSON file in the data folder and returns the object containing the data found in it

    :param filename: string -> name of the file to be read from
    :param subdir: string -> name of the subdirectory the file is located in. tailed with '/'
    :return: [dict] or dict
    """
    path = DIR + subdir + filename + '.json'
    mode = 'r'
    if not os.path.exists(path):
        raise Exception('file does not exist', filename, subdir)

    with open(path, mode) as infile:
        data = json.load(infile)
        return data


def validate_number_of_years(years):
    no_years = int(years)
    return max(min(no_years, 5), 1)


def get_start_end_date_touple(years):
    end_date = datetime.today()
    start_date = datetime(end_date.year - years, end_date.month, end_date.day)
    return start_date, end_date
