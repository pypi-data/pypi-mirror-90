import pandas as pd
from pandas import json_normalize
import numpy as np
from influxdb import DataFrameClient
import requests
from requests.exceptions import ConnectionError
import json
import signal
import sys
from datetime import datetime, timedelta
from time import sleep
import os
import threading
from collections import deque
from io import StringIO

class Config:
    db_host = 'localhost'
    db_port = 8086
    db_name = 'meteorology'
    stations = ['mythenquai', 'tiefenbrunnen']
    stations_force_query_last_entry = False
    stations_last_entries = {}
    keys_mapping = {
        'values.timestamp_cet.value': 'timestamp_cet',
        'values.air_temperature.value': 'air_temperature',
        'values.barometric_pressure_qfe.value': 'barometric_pressure_qfe',
        'values.dew_point.value': 'dew_point',
        'values.global_radiation.value': 'global_radiation',
        'values.humidity.value': 'humidity',
        'values.precipitation.value': 'precipitation',
        'values.water_temperature.value': 'water_temperature',
        'values.wind_direction.value': 'wind_direction',
        'values.wind_force_avg_10min.value': 'wind_force_avg_10min',
        'values.wind_gust_max_10min.value': 'wind_gust_max_10min',
        'values.wind_speed_avg_10min.value': 'wind_speed_avg_10min',
        'values.windchill.value': 'windchill'
    }
    historic_data_folder = '.' + os.sep + 'data'
    historic_data_chunksize = 10000
    historic_data_sleep_sec = 0
    client = None


def __set_last_db_entry(config, station, entry):
    current_last_time = __extract_last_db_day(config.stations_last_entries.get(station, None), station, None)
    entry_time = __extract_last_db_day(entry, station, None)

    if current_last_time is None and entry_time is not None:
        config.stations_last_entries[station] = entry
    elif current_last_time is not None and entry_time is not None and current_last_time < entry_time:
        config.stations_last_entries[station] = entry

def __get_last_db_entry(config, station):
    last_entry = None
    if not config.stations_force_query_last_entry:
        # speedup for Raspberry Pi - last entry query takes > 2 Sec.!
        last_entry = config.stations_last_entries.get(station, None)

    if last_entry is None:
        try:
            # we are only interested in time, however need to provide any field to make query work
            query = f'SELECT air_temperature FROM {station} ORDER BY time DESC LIMIT 1'
            last_entry = config.client.query(query)
        except:
            # There are influxDB versions which have an issue with above query
            print('An exception occurred while querying last entry from DB for ' + station + '. Try alternative approach.')
            query = f'SELECT * FROM {station} ORDER BY time DESC LIMIT 1'
            last_entry = config.client.query(query)

    __set_last_db_entry(config, station, last_entry)
    return last_entry

def __extract_last_db_day(last_entry, station, default_last_db_day):
    if last_entry is not None:
        val = None
        if isinstance(last_entry, pd.DataFrame):
            val = last_entry
        elif isinstance(last_entry, dict):
            val = last_entry.get(station, None)

        if val is not None:
            if not val.index.empty:
                return val.index[0].replace(tzinfo = None)

    return default_last_db_day

def __get_data_of_day(day, station):
    # convert to local time of station
    base_url = 'https://tecdottir.herokuapp.com/measurements/{}'
    day_str = day.strftime('%Y-%m-%d')
    print('Query ' + station + ' at ' + day_str)
    payload = {
        'startDate': day_str,
        'endDate': day_str
    }
    url = base_url.format(station)
    while True:
        try:
            response = requests.get(url, params = payload)
            if(response.ok):
                jData = json.loads(response.content)
                return jData
            else:
                response.raise_for_status()
                break
        except ConnectionError as e:
            print(f'Request for \'{e.request.url}\' failed. ({e.args[0].args[0]})\nTrying again in 10 seconds...')
            sleep(10)

def __define_types(data, date_format):
    if not data.empty:
        # convert cet to utc
        data['timestamp'] = pd.to_datetime(data['timestamp_cet'], format = date_format) - timedelta(hours = 1)
        data.drop('timestamp_cet', axis = 1, inplace = True)
        data.set_index('timestamp', inplace = True)

    for column in data.columns[0:]:
        if column != 'timestamp':
            data[column] = data[column].astype(np.float64)

    return data

def __clean_data(config, data_of_last_day, last_db_entry, station):
    normalized = json_normalize(data_of_last_day['result'])

    for column in normalized.columns[0:]:
        mapping = config.keys_mapping.get(column, None)
        if mapping is not None:
            normalized[mapping] = normalized[column]
        if mapping != column:
            normalized.drop(columns = column, inplace = True)

    normalized = __define_types(normalized, '%d.%m.%Y %H:%M:%S')

    # remove all entries older than last element
    last_db_entry_time = None
    if isinstance(last_db_entry, pd.DataFrame):
        last_db_entry_time = last_db_entry
    elif isinstance(last_db_entry, dict):
        last_db_entry_time = last_db_entry.get(station, None)
    last_db_entry_time = last_db_entry_time.index[0].replace(tzinfo = None)
    normalized.drop(normalized[normalized.index <= last_db_entry_time].index, inplace = True)

    return normalized

def __add_data_to_db(config, data, station):
    config.client.write_points(data, station, time_precision = 's', database = config.db_name)
    __set_last_db_entry(config, station, data.tail(1))

def __append_df_to_csv(data, csv_file_path, sep = ','):
    header = False
    if not os.path.isfile(csv_file_path):
        header = True

    data.to_csv(csv_file_path, mode = 'a', sep = sep, header = header, date_format = '%Y-%m-%dT%H:%M:%S')

def __import_csv_file(config, station, year):
    file_name = os.path.join(config.historic_data_folder, 'messwerte_' + station + '_' + year + '.csv')
    if os.path.isfile(file_name):
        print('\tLoad ' + file_name)
        for chunk in pd.read_csv(file_name, delimiter = ',', chunksize = config.historic_data_chunksize):
            chunk = __define_types(chunk, '%Y-%m-%dT%H:%M:%S')
            print('Add ' + station + ' from ' + str(chunk.index[0]) + ' to ' + str(chunk.index[-1]))
            __add_data_to_db(config, chunk, station)

            if config.historic_data_sleep_sec > 0:
                sleep(config.historic_data_sleep_sec)
    else:
        print(file_name + ' does not seem to exist.')

def __signal_handler(sig, frame):
    sys.exit(0)

def connect_db(config):
    """Connects to the database and initializes the client

    Parameters:
    config (Config): The Config containing the DB connection info

   """
    if config.client is None:
        # https://www.influxdata.com/blog/getting-started-python-influxdb/
        config.client = DataFrameClient(host = config.db_host, port = config.db_port)
        config.client.create_database(config.db_name)
        config.client.switch_database(config.db_name)

def clean_db(config):
    """Reads the historic data of the Wasserschutzpolizei Zurich from CSV files

    Parameters:
    config (Config): The Config containing the DB connection info and CSV folder info

   """
    config.client.drop_database(config.db_name)
    config.client.create_database(config.db_name)
    config.stations_last_entries.clear()

def import_historic_data(config):
    """Reads the historic data of the Wasserschutzpolizei Zurich from CSV files

    Parameters:
    config (Config): The Config containing the DB connection info and CSV folder info

   """
    # read historic data from files

    for station in config.stations:
        last_entry = __get_last_db_entry(config, station)

        if last_entry is None or not last_entry:
            print('Load historic data for ' + station + ' ...')

            __import_csv_file(config, station, '2007-2019')

            current_time = datetime.utcnow() + timedelta(hours = 1)
            running_year = 2020
            while running_year <= current_time.year:
                __import_csv_file(config, station, str(running_year))
                running_year += 1
        else:
            print('There is already data for ' + station + '. No historic data will be imported.')

        print('Historic data for ' + station + ' loaded.')


def import_latest_data(config, append_to_csv = False, periodic_read = False):
    """Reads the latest data from the Wasserschutzpolizei Zurich weather API

    Parameters:
    config (Config): The Config containing the DB connection info and CSV folder info
    append_to_csv (bool): Defines if the data should be appended to a CSV file
    periodic_read (bool): Defines if the function should keep reading after it imported the latest data (blocking through a sleep)

   """
    # access API for current data
    current_time = datetime.utcnow() + timedelta(hours = 1)
    current_day = current_time.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    last_db_days = [current_day] * len(config.stations)

    for idx, station in enumerate(config.stations):
        last_db_entry = __get_last_db_entry(config, station)
        last_db_days[idx] = __extract_last_db_day(last_db_entry, station, last_db_days[idx]) + timedelta(hours = 1)

    if periodic_read and threading.current_thread() is threading.main_thread():
        signal.signal(signal.SIGINT, __signal_handler)
        print('\nPress Ctrl+C to stop!\n')

    check_db_day = min(last_db_days)
    check_db_day = check_db_day.replace(hour = 0, minute = 0, second = 0, microsecond = 0)

    first_cycle = True
    last_cycle = False

    while True:
        # check if all historic data (retrieved from API) has been processed
        if not first_cycle and periodic_read and check_db_day >= current_day and not first_cycle:
            # once every 10 Min
            current_time = datetime.utcnow() + timedelta(hours = 1)
            sleep_until = current_time + timedelta(minutes = 10)
            # once per day
            # sleep_until = current_time + timedelta(days = 1)
            # sleep_until = sleep_until.replace(hour = 6, minute = 0, second = 0, microsecond = 0)
            sleep_sec = (sleep_until - current_time).total_seconds()

            print('Sleep for ' + str(sleep_sec) + 's (from ' + str(current_time) + ' until ' + str(sleep_until) + ') when next data will be queried.')
            sleep(sleep_sec)
            current_day = current_time.replace(hour = 0, minute = 0, second = 0, microsecond = 0)

        if not periodic_read and check_db_day >= current_day:
            if last_cycle:
                return
            last_cycle = True

        for idx, station in enumerate(config.stations):
            if last_db_days[idx].replace(hour = 0, minute = 0, second = 0, microsecond = 0) > check_db_day:
                continue
            last_db_entry = __get_last_db_entry(config, station)
            last_db_days[idx] = __extract_last_db_day(last_db_entry, station, last_db_days[idx])
            data_of_last_db_day = __get_data_of_day(check_db_day, station)

            normalized_data = __clean_data(config, data_of_last_db_day, last_db_entry, station)

            if normalized_data.size > 0:
                __add_data_to_db(config, normalized_data, station)
                if append_to_csv:
                    # save data as cet
                    normalized_data['timestamp_cet'] = normalized_data.index + timedelta(hours = 1)
                    normalized_data.set_index('timestamp_cet', inplace = True)

                    __append_df_to_csv(normalized_data, os.path.join(config.historic_data_folder ,'messwerte_' + station + '_' + str(normalized_data.index[0].year) + '.csv'))
                print('Handle ' + station + ' from ' + str(normalized_data.index[0]) + ' to ' + str(normalized_data.index[-1]))
            else:
                print('No new data received for ' + station)

        if check_db_day < current_day:
            check_db_day = check_db_day + pd.DateOffset(1)
        elif periodic_read and check_db_day >= current_day:
            check_db_day = datetime.utcnow() + timedelta(hours = 1)

        if first_cycle:
            first_cycle = False


def db_is_up_to_date(config):
    """Checks if all CSV files have been synced to database.

    Parameters:
    config (Config): The Config containing the DB connection info and CSV folder info

    """
    # read historic data from files
    max_file = {}

    for station in config.stations:
        last_entry = __get_last_db_entry(config, station)

        if last_entry is None or not station in last_entry or last_entry[station].empty:
            print('Database is empty.')
            return False

        file_name = os.path.join(config.historic_data_folder, 'messwerte_' + station + '_2007-2019.csv')
        if os.path.isfile(file_name):
            max_file[station] = file_name

        current_time = datetime.utcnow() + timedelta(hours = 1)
        running_year = 2020
        while running_year <= current_time.year:

            file_name = os.path.join(config.historic_data_folder, 'messwerte_' + station + '_' + str(running_year) + '.csv')
            if os.path.isfile(file_name):
                max_file[station] = file_name
            running_year += 1

        if station in max_file:
            with open(max_file[station], 'r') as f:
                headers = f.readline()
                last_line = deque(f, 1)
                last_line_csv = pd.read_csv(StringIO(headers + ''.join(last_line)))
                last_csv_entry = __define_types(last_line_csv, '%Y-%m-%dT%H:%M:%S')
                if last_csv_entry.index[0] != last_entry[station].index[0].replace(tzinfo = None):
                    return False

    return True
