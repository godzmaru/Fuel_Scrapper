from django.shortcuts import render
from django.http import HttpResponse, Http404
from .forms import Contact

# scrape function
from lxml import objectify
import urllib3
import pandas as pd

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()
container = []
param = {'Product', 'Suburb', 'Region', 'Brand', 'Surrounding', 'Day'}

def index(request):
    return render(request, 'fuel/index.html')

def contact(request):
    if request.method == 'POST':
        form = Contact(request.POST)
        if form.is_valid():
            pass
    else:
        form = Contact()
    return render(request, 'fuel/contact.html', {'form': form})
    
def fuel_table(request):
    fuel = remove_elem(get_fuel(Product = '1', Suburb = 'Murdoch', Day = 'today'))
    fuel = sorted(fuel, key=sort_prices) 
    return render(request, 'fuel/table.html', {'fuel':fuel,})

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
    data = list(temp.T.to_dict().values())
    return data

def sort_prices(elem):
    return elem['price']