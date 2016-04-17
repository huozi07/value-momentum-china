import data
import signals
import csv
import pandas
import numpy

df_sh, date_sh, dates = data.read_exchange_data('shanghai')

# sudden boom in shanghai stock count above 200
dates = [date for date in dates if date > numpy.datetime64('2000-01-01')]
counts = [signals.select_universe_value(df_sh, date_sh, random_date) for random_date in dates]

with open('shanghai_date_counts.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(zip(dates, counts))
