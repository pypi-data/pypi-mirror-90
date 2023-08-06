import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import json

def load_data():
    print('Load info about module mod1')
    from example_pkg import alist
    print(f'this is from pakage init - {alist}')

class Furniture(object):
    def __init__(self):
        self.name = 'My package to parse data from Ikea'
        self.dict={}
        
        self.header = {'user-agent':UserAgent().chrome}

    def __str__(self):
        return str(self.name)

    def parsing(self):
        '''
        Creating list of all items from ikea.ru with links

        '''
        try:

            page_name = 'https://www.ikea.com/ru/ru/cat/tovary-products/'
            page = requests.get(page_name,headers = self.header)
            data = page.text
            soup = BeautifulSoup(data,'lxml')
            products =[div.span.string for div in soup.find_all('ul', class_='vn-list--plain')]
            links =[div.a['href'] for div in soup.find_all('ul', class_='vn-list--plain')]
            self.dict = {div.span.string:div.a['href'] for div in soup.find_all('ul', class_='vn-list--plain')}

        except:
            print('Error while parsing the page')
        finally:
            return self.dict
    
    def parsing2(self,name):
        # x= Furniture()
        # dict =x.parsing()
        page_name = name # 'Диваны'
        page = requests.get(page_name,headers = self.header)
        data = page.text
        soup = BeautifulSoup(data,'lxml')
        products =[div.string for div in soup.find_all('span', class_='vn__nav__title')]
        links =[link.get('href') for link in soup.find_all('a',class_='vn-link vn__nav__link vn-6-grid-gap')]
        self.dict={product:link for product in products for link in links}
        
        return self.dict

    def parsing3(self,name):
        # x= Furniture()
        # dict =x.parsing2('Диваны')
        page_name = name # 'Все диваны'
        page = requests.get(page_name,headers = self.header)
        data = page.text
        soup = BeautifulSoup(data,'lxml')
        products =[div.string for div in soup.find_all('div', class_='range-revamp-header-section__title--small')]
        products_prices =[div.string for div in soup.find_all('span', class_='range-revamp-price__integer')]
        links=[div.a['href'] for div in soup.find_all('div', class_='range-revamp-product-compact__bottom-wrapper')]
        self.dict={product:link for product in products for link in links}
        
        return self.dict


        