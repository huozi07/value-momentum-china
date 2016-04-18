__author__ = 'linanqiu'

import numpy
import itertools
import pandas


def is_inactive(mnem, inactive_dates, date):
    if mnem not in inactive_dates:
        return False
    else:
        inactive_date = inactive_dates[mnem]
        inactive_date = numpy.datetime64(inactive_date)
        return date > inactive_date


def select_universe_value(dataframes, inactive_dates, date):
    assert isinstance(dataframes, dict)
    universe = [mnem for mnem in dataframes.keys()]

    # MV exists
    universe = [mnem for mnem in universe if 'MV' in dataframes[mnem].columns]

    # variable exists
    universe = [mnem for mnem in universe if 'MTBV' in dataframes[mnem].columns]

    # valid date
    ## not in inactive date
    universe = [mnem for mnem in universe if not is_inactive(mnem, inactive_dates, date)]
    ## value exists
    universe = [mnem for mnem in universe if not numpy.isnan(dataframes[mnem]['MTBV'][date])]

    # rank by market value and get 90% of market value
    universe = sorted(universe, key=lambda mnem: dataframes[mnem]['MV'][date], reverse=True)
    market_value_total = sum([dataframes[mnem]['MV'][date] for mnem in universe])
    market_value_sum = 0
    universe_90 = []
    for mnem in universe:
        market_value_sum += dataframes[mnem]['MV'][date]
        if market_value_sum < (market_value_total * 0.9):
            universe_90.append(mnem)

    universe = universe_90
    print('%s %s' % (date, len(universe)))

    # list of mnems
    return universe


def generate_signal_value_winner_loser(universe, dataframes, date):
    universe = sorted(universe, key=lambda mnem: dataframes[mnem]['MTBV'][date])
    bins = 10

    percentile_width = int(len(universe) / bins)

    winners = universe[:percentile_width]
    losers = universe[-percentile_width:]

    dicts = []
    for winner_mnem in winners:
        dicts.append({'mnem': winner_mnem, 'weight': 1 / (percentile_width * 2)})

    for loser_mnem in losers:
        dicts.append({'mnem': loser_mnem, 'weight': -1 / (percentile_width * 2)})
    signals = pandas.DataFrame(dicts)

    return signals


# value momentum everywhere formula
def generate_signal_value_ranked(universe, dataframes, date):
    # highest to lowest PTBV
    universe = sorted(universe, key=lambda mnem: dataframes[mnem]['MTBV'][date], reverse=True)
    ranks = range(1, len(universe) + 1)
    ranks_sum = sum(ranks) / len(ranks)
    c = (4 / sum(ranks))

    signals = pandas.DataFrame({'mnem': universe, 'rank': ranks})

    signals['weight'] = signals.apply(lambda row: c * (row['rank'] - ranks_sum), axis=1)

    return signals


def select_universe_momentum(dataframes, inactive_dates, date):
    assert isinstance(dataframes, dict)
    universe = [mnem for mnem in dataframes.keys()]

    # MV exists
    universe = [mnem for mnem in universe if 'MV' in dataframes[mnem].columns]

    # variable exists
    universe = [mnem for mnem in universe if 'P' in dataframes[mnem].columns]

    # valid date
    ## not in inactive date
    universe = [mnem for mnem in universe if not is_inactive(mnem, inactive_dates, date)]
    ## value exists
    universe = [mnem for mnem in universe if not numpy.isnan(dataframes[mnem]['P'][date])]
    universe = [mnem for mnem in universe if not numpy.isnan(dataframes[mnem]['P'][date - numpy.timedelta64(4, 'W')])]
    universe = [mnem for mnem in universe if not numpy.isnan(dataframes[mnem]['P'][date - numpy.timedelta64(52, 'W')])]

    # rank by market value and get 90% of market value
    universe = sorted(universe, key=lambda mnem: dataframes[mnem]['MV'][date], reverse=True)
    market_value_total = sum([dataframes[mnem]['MV'][date] for mnem in universe])
    market_value_sum = 0
    universe_90 = []
    for mnem in universe:
        market_value_sum += dataframes[mnem]['MV'][date]
        if market_value_sum < (market_value_total * 0.9):
            universe_90.append(mnem)

    universe = universe_90
    print('%s %s' % (date, len(universe)))

    # list of mnems
    return universe


def momentum_return(mnem, dataframes, date, weeks_a, weeks_b):
    p_a = dataframes[mnem]['P'][date - numpy.timedelta64(weeks_a, 'W')]
    p_b = dataframes[mnem]['P'][date - numpy.timedelta64(weeks_b, 'W')]

    return (p_a - p_b) / p_b


def generate_signal_momentum(universe, dataframes, date):
    # highest to lowest PTBV
    momentums = [{'mnem': mnem, '2-12': momentum_return(mnem, dataframes, date, 9, 52)} for mnem in universe]
    # ascending order of 2-12 return. smallest return first.
    momentums = sorted(momentums, key=lambda momentum: momentum['2-12'])
    universe = [momentum['mnem'] for momentum in momentums]
    momentums = [momentum['2-12'] for momentum in momentums]
    ranks = range(1, len(universe) + 1)
    ranks_sum = sum(ranks) / len(ranks)
    c = (4 / sum(ranks))

    signals = pandas.DataFrame({'mnem': universe, '2-12': momentums, 'rank': ranks})

    signals['weight'] = signals.apply(lambda row: c * (row['rank'] - ranks_sum), axis=1)

    return signals
