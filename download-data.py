import pydatastream
from pydatastream import Datastream
import os

credentials = {}
with open('credentials.txt', 'r') as credentials_file:
  line = credentials_file.readline().split(',')
  credentials['username'] = line[0]
  credentials['password'] = line[1]

DWE = Datastream(username=credentials['username'], password=credentials['password'])
DWE.raise_on_error = False

DATATYPES = ['P', 'MV', 'PE', 'VA', 'VO', 'PTBV', 'MTBV']

def scrape_index(index_name):
  print 'Querying index %s' % (index_name)
  constituents = DWE.get_constituents(index_name)
  print 'Writing index_%s.csv' % (index_name)
  constituents.to_csv('csvs/index_%s.csv' % index_name)

  stock_mnems = list(constituents['MNEM'])
  for stock_mnem in stock_mnems:
    filename = 'stock_%s_%s.csv' % (index_name, stock_mnem)
    filename = filename.replace(':', '-')

    # if os.path.isfile('csvs/%s' % filename):
    #   print 'Stock data already exists for %s' % (stock_mnem)
    #   continue

    print 'Querying stocks data for %s' % (stock_mnem)
    try:
      stock_data = DWE.fetch([stock_mnem], DATATYPES, date_from='1990-01-01', freq='W')
      filename = 'stock_%s_%s.csv' % (index_name, stock_mnem)
      filename = filename.replace(':', '-')
      print 'Writing %s' % filename
      stock_data.to_csv('csvs/%s' % (filename))
    except KeyError, e:
      print 'Key Error occured for %s_%s' % (index_name, stock_mnem)
    except pydatastream.pydatastream.DatastreamException, e:
      print 'DatastreamException occured for %s_%s' % (index_name, stock_mnem)

scrape_index('CHSCOMP')
scrape_index('CHZCOMP')
scrape_index('CHSASHR')
scrape_index('CHZASHR')
