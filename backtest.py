__author__ = 'linanqiu'

import pandas


def quantity(row, dataframes, date):
    # quantity to buy is proportional to P / w per stock
    mnem = row['mnem']
    weight = row['weight']
    price = dataframes[mnem]['P'][date]
    q = weight / price
    return q


def row_return(row, sum_positive_weights, sum_negative_weights):
    if row['weight'] > 0:
        return row['profit'] * abs(row['weight']) / sum_positive_weights
    else:
        return row['profit'] * abs(row['weight']) / sum_negative_weights


# assume 1 dollar long, 1 dollar short
def period_return(signal, dataframes, date_t0, date_t1):
    signal['price_t0'] = signal.apply(lambda row: dataframes[row['mnem']]['P'][date_t0], axis=1)
    signal['price_t1'] = signal.apply(lambda row: dataframes[row['mnem']]['P'][date_t1], axis=1)
    signal['return'] = signal.apply(lambda row: (row['price_t1'] - row['price_t0']) / row['price_t0'], axis=1)
    return sum(signal['return'] * signal['weight'])
