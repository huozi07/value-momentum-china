__author__ = 'linanqiu'

import numpy


def select_universe_value(dataframes, inactive_dates, date):
    assert isinstance(dataframes, dict)
    universe = [mnem for mnem in dataframes.keys()]

    # MV exists
    universe = [mnem for mnem in universe if 'MV' in dataframes[mnem].columns]

    # variable exists
    universe = [mnem for mnem in universe if 'PTBV' in dataframes[mnem].columns]

    # valid date
    ## not in inactive date
    universe = [mnem for mnem in universe if mnem not in inactive_dates]
    ## value exists
    universe = [mnem for mnem in universe if not numpy.isnan(dataframes[mnem]['PTBV'][date])]

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
    print(len(universe))

    # list of mnems
    return universe
