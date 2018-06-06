from django.shortcuts import render
from django.http import HttpResponse, Http404
from .forms import Contact

# scrape function
from lxml import objectify
import urllib3
import json
from . import params

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()
param = {'Product', 'Suburb', 'Region', 'Brand', 'Surrounding', 'Day'}
views = ['fuel/mithril.html', 'fuel/jquery.html', 'fuel/table.html']

def index(request):
    suburb = params.get_suburb()
    return render(request, 'fuel/index.html', {'suburb':suburb})

def contact(request):
    if request.method == 'POST':
        form = Contact(request.POST)
        if form.is_valid():
            pass
    else:
        form = Contact()
    return render(request, 'fuel/contact.html', {'form': form})

def mithril_index(request):
    suburb = params.get_suburb()
    brand = params.get_brand()
    return render(request, 'fuel/mithril.html', {'suburb': suburb, 'brand': brand})

def mithril_json(request):
    product = request.GET.get("Product", 1)
    fuel = get_fuel(Product = product, Day = 'today')
    fuel = json.dumps(sorted(fuel, key=sort_prices))
    return HttpResponse(fuel)

def jquery_index(request):
    product = request.GET.get('Product',1)
    day = request.GET.get('Day', 'today')
    suburb = params.get_suburb()
    fuel = get_fuel(Product = product, Day = day)
    fuel = json.dumps(sorted(fuel, key=sort_prices))
    return render(request, 'fuel/jquery.html', {'fuel':fuel, 'suburb':suburb})  

def fuel_table(request):
    product = request.GET.get('Product', 1)
    suburb = request.GET['Suburb']
    day = request.GET.get('Day','today')
    fuel = get_fuel(Product = product, Suburb = suburb, Day = day)
    fuel = sorted(fuel, key=sort_prices) 
    return render(request, 'fuel/table.html', {'fuel':fuel })

def get_fuel(**param):
    container = []
    for key, value in param.items():
        response = http.request('GET','https://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS', fields = param)
        root = objectify.fromstring(response.data)

    for each in root.channel.item:
        data = (each.getchildren())
        fuel_data = {d.tag: d.text for d in data if d.tag != 'description' and d.tag != 'site-features' and d.tag != 'title' and d.tag != 'trading-name'}
        container.append(fuel_data)
    return container

def sort_prices(elem):
    return elem['price']