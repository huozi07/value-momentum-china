import data
import signals
import csv

df_sh, date_sh, dates = data.read_exchange_data('shanghai')

counts = [signals.select_universe_value(df_sh, date_sh, random_date) for random_date in dates]

with open('shanghai_date_counts.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(zip(dates, counts))
