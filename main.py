from fastapi import FastAPI, HTTPException
from scraper import CoursDeviseScraper
from scraper1 import CurrencyConverterScraper

app = FastAPI()

# Initialisation de l'instance de la classe avec l'URL du site
scraper = CoursDeviseScraper(url='https://www.bceao.int/fr/cours/cours-des-devises-contre-Franc-CFA-appliquer-aux-transferts')
scraper1 = CurrencyConverterScraper()

# Accueil
@app.get('/')
async def bienvenu():
    return 'Soyez les bienvenus sur API des Cours des Devises!'

# API du scraping
@app.get('/api/scrape')
async def scrape_data(Devise: str, Date: str):
    try:
        scraper.scrape_data(devise=Devise, date=Date)
        scraper.save_data('data.json')
        return {'message': 'Scraping terminé avec succès', 'data': scraper.data[Date]}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# API du scraping puis le retour de la requête
@app.get('/api/coursdevises')
async def get_cours_devise(Devise: str, Date: str):
    try:
        scraper.scrape_data(devise=Devise, date=Date)
        return {
            "Devise": f"{Devise}/XOF",
            "Echange": scraper.data[Date]
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# API du scraping de conversion des devises
@app.get('/api/convertion_devise')
async def convert(Montant: int, Devise_montant: str, Devise_voulue: str):
    url = f'https://www.xe.com/fr/currencyconverter/convert/?Amount={Montant}&From={Devise_montant}&To={Devise_voulue}'
    try:
        result = scraper1.get_donnee_converties(url)
        montant_sortis = result[0]['Montant_sortis']
        return f"Resultat en {Devise_voulue}: {montant_sortis}"
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
