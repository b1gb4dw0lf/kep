from bs4 import BeautifulSoup
import requests

from django.core.management.base import BaseCommand, CommandError
from home.models import SolarPanel, Battery, Inverter

INCH_TO_CM = 2.54
LB_TO_KG = 0.453592
class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        pass

    def fill_solar_panels(self):
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

    def fill_batteries(self):
        response = requests.get('https://www.wholesalesolar.com/shop/batteries')
        page_html = response.text
        soup = BeautifulSoup(page_html, 'html.parser')
        rows = soup.find_all('tr', attrs={'class': 'product-row'})
        for row in rows:
            kwargs = {}
            img = row.find('img', attrs={'class': 'img-responsive lazy'})
            kwargs['name'] = row.find('div', attrs={'class': 'product-row-link'}).text
            kwargs['image_url'] = img.get('data-src')

            kwargs['voltage'] = float(row.find_all('td')[2].text.split('VDC')[0])
            kwargs['amper_hours'] = float(row.find_all('td')[3].text.split('Ah')[0])
            kwargs['kind'] = row.find_all('td')[4].text
            try:
                price = float(row.find('div', attrs={'class': 'price'}).text.replace('$', ''))
            except:
                price = None
            if price is None:
                continue
            else:
                kwargs['price'] = price

            Battery.objects.get_or_create(**kwargs)

    def fill_inverters(self):
        response = requests.get('https://www.wholesalesolar.com/shop/inverters')
        page_html = response.text
        soup = BeautifulSoup(page_html, 'html.parser')
        rows = soup.find_all('tr', attrs={'class': 'product-row'})
        for row in rows:
            kwargs = {}
            #import pdb;pdb.set_trace()
            img = row.find('img', attrs={'class': 'img-responsive lazy'})
            kwargs['name'] = row.find('div', attrs={'class': 'product-row-link'}).text
            kwargs['image_url'] = img.get('data-src')

            watts_str = row.find_all('td')[2].text.split('W')[0]
            if not watts_str:
                continue
            kwargs['watts'] = float(watts_str)
            try:
                kwargs['input_voltage'] = float(row.find_all('td')[3].text.lower().split('vdc')[0])
            except:
                continue
            output_voltage = row.find_all('td')[4].text
            if '/' in output_voltage:
                output_voltage = float(output_voltage.split('/')[0])
            else:
                output_voltage = float(output_voltage.replace('AC', '')[0])
            kwargs['output_voltage'] = output_voltage
            kwargs['kind'] = row.find_all('td')[5].text
            try:
                price = float(row.find('div', attrs={'class': 'price'}).text.replace('$', ''))
            except:
                price = None
            if price is None:
                continue
            else:
                kwargs['price'] = price

            Inverter.objects.get_or_create(**kwargs)

    def handle(self, *args, **options):
        self.fill_solar_panels()
        self.fill_batteries()
        self.fill_inverters()
