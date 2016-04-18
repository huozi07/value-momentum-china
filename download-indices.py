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

chsashr_pi = DWE.fetch('CHSASHR', ['PI'], date_from='1990-01-01', freq='W')
chsashr_pi.to_csv('csvs/index_chsashr.csv')

chzashr_pi = DWE.fetch('CHZASHR', ['PI'], date_from='1990-01-01', freq='W')
chsashr_pi.to_csv('csvs/index_chzashr.csv')
