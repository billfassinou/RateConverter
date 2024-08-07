from fastapi import FastAPI, HTTPException
from scraper import CurrencyConverterScraper

app = FastAPI()

# Initialisation de l'instance de la classe avec l'URL du site
scraper = CurrencyConverterScraper()

# Accueil
@app.get('/')
async def bienvenu():
    return f"Bienvenus sur l'API de conversions de devises!"

# API du scraping de conversion des devises
@app.get('/api/convertion_devise')
async def convert(Amont: int, Currency_to_convert: str, Expected_Currency: str):
    url = f'https://www.xe.com/fr/currencyconverter/convert/?Amount={Amont}&From={Currency_to_convert}&To={Expected_Currency}'
    try:
        result = scraper.get_donnee_converties(url)
        montant_sortis = result[0]['Montant_sortis']
        return f"Resultat en {Expected_Currency}: {montant_sortis}"
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
