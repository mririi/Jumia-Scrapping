from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests

def get_data(query_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(query_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    results = []
    for product in soup.find_all('div', {'class': 'sku -gallery'}):
        title = product.find('div', {'class': 'sku -gallery -has-offers'}).text.strip()
        price = product.find('div', {'class': 'c-prd-price'}).text.strip()
        brand = product.find('div', {'class': 'c-prd-brand'}).text.strip()
        link = product.find('a', {'class': 'core'})['href']
        results.append({'title': title, 'price': price, 'brand': brand, 'link': link})
    return results

def home(request):
    if request.method == 'POST':
        brand = request.POST.get('brand')
        price = request.POST.get('price')
        query_url = f'https://www.jumia.tn/fr/catalog/?q={brand}&price={price}'
        results = get_data(query_url)
        context = {'results': results}
        return render(request, 'home.html', context)
    else:
        return render(request, 'home.html')
