import pydatastream
from pydatastream import Datastream
import os
import csv

credentials = {}
with open('credentials.txt', 'r') as credentials_file:
  line = credentials_file.readline().split(',')
  credentials['username'] = line[0]
  credentials['password'] = line[1]

DWE = Datastream(username=credentials['username'], password=credentials['password'])
DWE.raise_on_error = False
INACTIVE_DATE = ['WC07015']

DATATYPES = ['P', 'MV', 'PE', 'VA', 'VO', 'PTBV', 'MTBV']

shenzhen_equities_symbols = []

with open('shenzhen-equities-rmb.csv', 'r') as shenzhen_equities_csv:
    reader = csv.DictReader(shenzhen_equities_csv)
    shenzhen_equities_symbols = [line['Symbol'] for line in reader]

    for stock_mnem in shenzhen_equities_symbols:
      filename = 'stock_%s_%s.csv' % ('shenzhen', stock_mnem)
      filename = filename.replace(':', '-')

      if os.path.isfile('csvs/%s' % filename):
        print 'Stock data already exists for %s' % (stock_mnem)
        continue

      print 'Querying stocks data for %s' % (stock_mnem)
      try:
        stock_data = DWE.fetch([stock_mnem], DATATYPES, date_from='1990-01-01', freq='W')
        filename = 'stock_%s_%s.csv' % ('shenzhen', stock_mnem)
        filename = filename.replace(':', '-')
        print 'Writing %s' % filename
        stock_data.to_csv('csvs/%s' % (filename))
      except KeyError, e:
        print 'Key Error occured for %s_%s' % ('shenzhen', stock_mnem)
      except pydatastream.pydatastream.DatastreamException, e:
        print 'DatastreamException occured for %s_%s' % ('shenzhen', stock_mnem)

shenzhen_equities_inactive_dates = DWE.fetch(shenzhen_equities_symbols, INACTIVE_DATE, static=True)
shenzhen_equities_inactive_dates.to_csv('csvs/shenzhen_equities_inactive_dates.csv')
