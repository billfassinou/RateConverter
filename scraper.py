import requests
from bs4 import BeautifulSoup

class CurrencyConverterScraper:
    def __init__(self):
        pass
    
    def get_soup(self,url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup
    
    def get_donnee_converties(self, url):
        soup = self.get_soup(url)
        elements = soup.find_all('main', class_='sc-d5cf72bb-3 lmBDhC')
        data = []
        
        for elt in elements:
            montant_entres = elt.find('div', class_='sc-73a056d4-0 sc-b8d6d0bc-0 eVknbT eoNUEg').text
            devise = elt.find('div', id='midmarketToCurrency').text
            montant_sortis = elt.find('p', class_='sc-e08d6cef-1 fwpLse').text
            data.append({
                'Montant_entres': montant_entres,
                'Devise': devise,
                'Montant_sortis': montant_sortis
            })
        
        return data
    
    