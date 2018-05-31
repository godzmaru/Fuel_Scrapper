#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 28 09:28:27 2018

Fuel Parameters

@author: hendrawahyu
"""

from bs4 import BeautifulSoup
import urllib3

http = urllib3.PoolManager()
url = "https://www.fuelwatch.wa.gov.au/fuelwatch/pages/public/quickSearch.jspx"
response = http.request('GET', url)
soup = BeautifulSoup(response.data)

def get_suburb():    
    suburb = soup.find("select", {"id":"quickSearch:location"})
    options = suburb.find_all("option")
    values = [v.get("value") for v in options]
    return values

def get_brand():
    brand = soup.find("select", {"id":"quickSearch:brand"})
    options = brand.find_all("option")
    text = [v.text for v in options]
    return text