from bs4 import BeautifulSoup
import requests

from django.core.management.base import BaseCommand, CommandError
from home.models import SolarPanel

INCH_TO_CM = 2.54
LB_TO_KG = 0.453592
class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        response = requests.get('https://www.wholesalesolar.com/shop/solar-panels')
        page_html = response.text
        soup = BeautifulSoup(page_html, 'html.parser')
        rows = soup.find_all('tr', attrs={'class': 'product-row'})
        for row in rows:
            kwargs = {}
            img = row.find('img', attrs={'class': 'img-responsive lazy'})
            kwargs['name'] = row.find('div', attrs={'class': 'product-row-link'}).text
            kwargs['image_url'] = img.get('data-src')

            kwargs['watt'] = float(row.find_all('td')[2].text.split('W')[0])

            size_weight = row.find_all('td')[3]
            kwargs['width'] = float(size_weight.text.split('\xa0×\xa0')[0]) * INCH_TO_CM
            kwargs['height'] = float(size_weight.text.split('\xa0×\xa0')[1]) * INCH_TO_CM
            kwargs['thickness'] = float(
                size_weight.text.split('\xa0×\xa0')[2].split('\xa0in')[0]) * INCH_TO_CM
            kwargs['weight'] = float(
                size_weight.text.split('\xa0×\xa0')[2].split('\xa0in')[1].split(' ')[0]) * LB_TO_KG

            material = 'mono-crystalline'
            if 'poly' in kwargs['name']:
                material = 'poly-cristalline'

            kwargs['material'] = material

            try:
                price = float(row.find('div', attrs={'class': 'price'}).text.replace('$', ''))
            except:
                price = None
            if price is None:
                continue
            else:
                kwargs['price'] = price

            SolarPanel.objects.get_or_create(**kwargs)
