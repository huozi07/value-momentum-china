import data
import signals
import csv
import pandas
import numpy
import pickle as pickle
import backtest

df_sh, date_sh, dates = data.read_exchange_data('shanghai')
pickle.dump(df_sh, open('temp/df_sh.pkl', 'wb'))
pickle.dump(date_sh, open('temp/date_sh.pkl', 'wb'))
df_sh = pickle.load(open('temp/df_sh.pkl', 'rb'))
date_sh = pickle.load(open('temp/date_sh.pkl', 'rb'))


# sudden boom in shanghai stock count above 200
dates = [date for date in dates if date > numpy.datetime64('2000-01-01')]
pickle.dump(dates, open('temp/dates.pkl', 'wb'))
dates = pickle.load(open('temp/dates.pkl', 'rb'))

universes = [signals.select_universe_value(df_sh, date_sh, random_date) for random_date in dates]
pickle.dump(universes, open('temp/universes_sh.pkl', 'wb'))
universes = pickle.load(open('temp/universes_sh.pkl', 'rb'))

# signals_value_sh = [signals.generate_signal_value_winner_loser(universe, df_sh, date) for universe, date in zip(
# universes, dates)]
# pickle.dump(signals_value_sh, open('temp/signals_value_sh.pkl', 'wb'))
# signals_value_sh = pickle.load(open('temp/signals_value_sh.pkl', 'rb'))

signals_value_sh = [signals.generate_signal_value_ranked(universe, df_sh, date) for universe, date in zip(
universes, dates)]
pickle.dump(signals_value_sh, open('temp/signals_value_sh.pkl', 'wb'))
signals_value_sh = pickle.load(open('temp/signals_value_sh.pkl', 'rb'))

# period_return = backtest.period_return(signals_value_sh[0], df_sh, dates[0], dates[0 + 4])
# print(period_return)

# period_returns = []
#
# for i in range(1, len(dates)):
#     date_t0 = dates[i-1]
#     date_t1 = dates[i]
#     period_return = backtest.period_return(signals_value_sh[i], df_sh, date_t0, date_t1)
#     period_returns.append(period_return)
#
# pickle.dump(period_returns, open('temp/period_returns_sh.pkl', 'wb'))
