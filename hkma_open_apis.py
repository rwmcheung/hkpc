# -*- coding: utf-8 -*-
"""HKMA Open APIs.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/kenwkliu/ideas/blob/master/colab/HKMA-OpenAPIs.ipynb
"""

# Visualize the data from HKMA APIs
# https://apidocs.hkma.gov.hk/

import math
import pandas as pd

# interative map
import folium

# bypass SSL cert
import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
  ssl._create_default_https_context = ssl._create_unverified_context

# Enable Google interactive table
from google.colab import data_table
data_table.enable_dataframe_formatter()

# a library to convert the Latitude and Longitude from degree format to decimal
!pip install dms2dec
from dms2dec.dms_convert import dms2dec

# Get the daily exchange rate from HKMA 
url = 'https://api.hkma.gov.hk/public/market-data-and-statistics/monthly-statistical-bulletin/er-ir/er-eeri-daily'

# Read the json URL output into a dataframe 
df = pd.read_json(url)
print(df)

# Extract the record result into another dataframe
ccyDf = pd.DataFrame(df.loc['records', 'result'])
ccyDf.set_index('end_of_day', inplace=True)

# Display the major ccy
ccyDf[['usd', 'gbp', 'cad', 'aud', 'cny', 'jpy', 'eur']]

# sort the date in asc order and plot the graph
ccyDf[['gbp']].sort_index().plot(figsize = (12, 8))

# Browse other HKMA examples: https://apidocs.hkma.gov.hk/apidata/
# and find the corresponding data link in the https://apidocs.hkma.gov.hk/

# Hospitals info from HA
url = 'http://www.ha.org.hk/opendata/facility-hosp.json'
dfHospital = pd.read_json(url)
dfHospital

# Create an interactive folium map and zoom to HK
HK_LAT, HK_LONG = 22.3, 114.2
hmap = folium.Map(location=[HK_LAT, HK_LONG], zoom_start=11)

# From each row of the footbook dataframe, pin the location in the map with the name and opening_time by a tooltip 
for row in dfHospital.itertuples():
  tip = row.institution_eng
  #tip = row.institution_tc
  if math.isnan(row.latitude) == False and math.isnan(row.longitude) == False:
    folium.Marker([row.latitude, row.longitude], tooltip=tip).add_to(hmap)

hmap

# save the hospital map
hmap.save('hospital.html')

# Other examples
# All other JSON format: https://data.gov.hk/en-datasets/format/json
# All other CSV format: https://data.gov.hk/en-datasets/format/csv

# Idea
# Use the Gov open data (such as pollution index, beach water quality) to track health for pharmaceutical stocks