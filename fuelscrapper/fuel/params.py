#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 28 09:28:27 2018

Fuel Parameters

@author: hendrawahyu
"""

from bs4 import BeautifulSoup
import urllib3

def get_suburb():
    http = urllib3.PoolManager()
    url = "https://www.fuelwatch.wa.gov.au/fuelwatch/pages/public/quickSearch.jspx"
    response = http.request('GET', url)

    # Beautiful soup
    soup = BeautifulSoup(response.data)

    # Suburb
    suburb = soup.find("select", {"id":"quickSearch:location"})
    options = suburb.find_all("option")
    values = [v.get("value") for v in options]
    return values
