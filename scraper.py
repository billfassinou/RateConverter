from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

class CoursDeviseScraper:
    def __init__(self, url: str):
        self.url = url
        self.driver = webdriver.Chrome()
        self.data = {}

    def close(self):
        self.driver.quit()

    def is_weekend_or_holiday(self, date: str):
        holidays = ["2024-01-01", "2024-03-31", "2024-04-01", "2024-05-01", "2024-06-01", "2024-12-25"]
        return time.strptime(date, '%Y-%m-%d').tm_wday >= 5 or date in holidays

    def scrape_data(self, devise: str, date: str):
        self.driver.get(self.url)
        wait = WebDriverWait(self.driver, 10)

        year, month, day = map(int, date.split('-'))

        if self.is_weekend_or_holiday(date):
            raise ValueError("La date sélectionnée est un week-end ou un jour férié.")

        rectangular_frame = wait.until(EC.element_to_be_clickable((By.ID, 'date_picker')))
        rectangular_frame.click()

        tds = self.driver.find_elements(By.CSS_SELECTOR, 'table.ui-datepicker-calendar td')
        day_td = [td for td in tds if td.text == str(day) and td.is_displayed()]
        
        if not day_td:
            raise ValueError(f"Le jour sélectionné n'est pas disponible pour le scraping.")

        try:
            self.driver.execute_script("arguments[0].click();", day_td[0])

            table = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="box_cours"]/table')))
            rows = table.find_elements(By.TAG_NAME, 'tr')

            for row in rows:
                cells = row.find_elements(By.TAG_NAME, 'td')
                if len(cells) == 3 and cells[0].text == devise:
                    self.data[date] = {
                        #'Devise': cells[0].text,
                        'Achat': cells[1].text,
                        'Vente': cells[2].text
                    }
                    break

        except Exception as e:
            raise ValueError(f"Une erreur s'est produite lors du scraping: {e}")

    def save_data(self, file_path: str):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
