from bs4 import BeautifulSoup
import requests
from db_handle import *

def search_med(medicine):
    base_url = "https://www.drugs.com/"
    search_url = f"{base_url}{medicine}.html"
    req = requests.get(search_url)

    if req.status_code != 200:
        print(f"Failed to retrieve search results for {medicine}. Status code: {req.status_code}")
        return
    
    soup = BeautifulSoup(req.content, "lxml")
    
    medicine_data = {
        'medicine': medicine,
        'uses': [],
        'warnings': [],
        'dosage': [],
        'side-effects': []
    }
    
    sections = ['uses', 'warnings', 'dosage', 'side-effects']
    current_section = None
    
    for element in soup.find_all(['h2', 'p', 'li']):
        if element.name == 'h2':
            section_id = element.get('id')
            if section_id in sections:
                current_section = section_id
            else:
                current_section = None
        elif element.name == 'li' and current_section == 'side-effects':
            medicine_data[current_section].append(element.get_text(strip=True))
        elif element.name == 'p' and current_section and current_section != 'side-effects':
            medicine_data[current_section].append(element.get_text(strip=True))
            
    insert_medicine_data(medicine, medicine_data)
    
    return medicine_data

# Example usage
# search_med('pratham')
# search_med('aspirin')