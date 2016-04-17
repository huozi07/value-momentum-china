__author__ = 'linanqiu'

import glob
import os

import pandas


def read_exchange_data(exchange='shanghai'):
    inactive_dates = pandas.read_csv('./csvs/%s_equities_inactive_dates.csv' % exchange)
    assert isinstance(inactive_dates, pandas.DataFrame)
    inactive_dates = inactive_dates[pandas.notnull(inactive_dates['WC07015'])]
    inactive_dates['WC07015'] = pandas.to_datetime(inactive_dates['WC07015'])
    inactive_dates = inactive_dates.set_index('SYMBOL')['WC07015'].to_dict()

    dataframes = {}

    for csv_file in glob.glob('./csvs/stock_%s_*.csv' % exchange):
        dataframe = pandas.read_csv(csv_file)
        assert isinstance(dataframe, pandas.DataFrame)
        if not dataframe.empty:
            dataframe['date'] = dataframe['Unnamed: 0']
            dataframe['date'] = pandas.to_datetime(dataframe['date'])
            dataframe = dataframe.drop('Unnamed: 0', axis=1)
            dataframe = dataframe.set_index('date')
            mnem = os.path.splitext(os.path.basename(csv_file))[0].split('_')[2].replace('-', ':')
            dataframes[mnem] = dataframe

    dates = next(iter(dataframes.values())).index.values

    return dataframes, inactive_dates, dates
