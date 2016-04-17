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

    # rank by market value and get top 100
    universe = sorted(universe, key=lambda mnem: dataframes[mnem]['MV'][date], reverse=True)
    universe = universe[:100]

    # list of mnems
    return universe
