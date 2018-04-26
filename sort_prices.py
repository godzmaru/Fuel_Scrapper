#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 18:39:36 2018

@author: hendrawahyu
"""
# =============================================================================
# 
# Product: Each fuel type has a unique code - to specify which one you are interested in, make sure you include this parameter. This defaults to 1, so if you don't specify a product, you will get ULP. The codes are:
# 
# 1 - Unleaded Petrol
# 2 - Premium Unleaded
# 4 - Diesel
# 5 - LPG
# 6 - 98 RON
# 10 - E85
# 11 - Brand diesel
# 
# Suburb: This is the suburb you want to receive prices for. 
# A full list of suburbs can be found at 
# http://www.fuelwatch.wa.gov.au/fuelwatch/pages/public/quickSearch.jspx (just look through the dropdown list of suburbs)
# 
# Region: You can use region instead of suburb if you would like prices for a particular town 
# or shire that FuelWatch covers. Each region has an ID - use that ID to get prices for the area. 
# The list of regions is long, and has been included at the bottom of this post.
# 
# Brand: If you want to restrict the results to only include service stations with a particular
# brand, you can specify it here. Each brand has an ID - use that ID to get prices for sites with 
# that particular brand. The list of brands is at the bottom of this page.
# 
# Surrounding: Set this to yes if you want to include surrounding suburbs in your search, 
# set this to no if you only want prices for that particular suburb. By default, this is 
# set to yes. (So for example, if your search is for Cannington prices, then by default, 
# it will also return prices for Bentley, Beckenham, etc. Setting it to no will mean you 
# only get prices for Cannington)
# 
# =============================================================================
from lxml import objectify
import urllib3

# for test purposes
import pandas as pd

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()
container = []
coord = []
param = {'Product', 'Suburb', 'Region', 'Brand', 'Surrounding', 'Day'}

def get_fuel(**param):
    for key, value in param.items():
        response = http.request('GET','https://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS', fields = param)
        root = objectify.fromstring(response.data)

    for each in root.channel.item:
        fuel_data = {}
        data = (each.getchildren())
        for d in data:    
            fuel_data[d.tag] = d.text
        container.append(fuel_data)
    return container

def remove_elem(container):
    # convert to Panda to eliminate 
    temp = pd.DataFrame(container, columns=['address', 'brand', 'date', 'latitude', 'longitude', 'location', 'phone', 'price'])
    temp_c = pd.DataFrame(container, columns = ['longitude','latitude'])
    data = list(enumerate(temp.T.to_dict().values()))
    coord = list(enumerate(temp_c.T.to_dict().values()))
    return data, coord
    
#def sort_prices(elem):
#    return elem['price']

# different sorting
fuel_info = get_fuel(Product = '1', Suburb = 'Murdoch', Day = 'today')
fuel_info2 = sorted(fuel_info, key=sort_prices)   
fuel_info3 = sorted(fuel_info, key = lambda x: x['brand'], reverse = True)
fuel_info4, coord = remove_elem(fuel_info)
 
# put into dataframe for convenience
a = pd.DataFrame(fuel_info, columns = ['brand', 'price'])
