from nltk.corpus import wordnet
import spacy
import random
import sys
import os
import pymongo
from bs4 import BeautifulSoup
import requests
# from medicine_data_extractor import *
# from db_handle import *
module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modules'))
sys.path.append(module_path)
from augmented_data_generation import *
from keywords import *

# Load spaCy model
nlp = spacy.load("en_core_web_lg")

# static data
intent_data = [
    {
        'intent': 'uses',
        'patterns': 
            ["What are the uses of _?", "How is _ used?", "What conditions does _ treat?", "What are the benefits of _?", "What can _ be used for?", "For what purposes is _ prescribed?", "What is _ used for?", "What conditions can _ help with?", "What are the indications for _?", "Why is _ prescribed?", "What does _ help with?", "What ailments does _ address?", "What medical conditions does _ treat?", "In what situations is _ recommended?", "What are the therapeutic uses of _?"],
        'keywords': 
            ['purpose', 'habit', 'expend', 'utilisation', 'utilization', 'apply', 'employ', 'practice', 'usage', 'enjoyment', 'exercise', 'utilize', 'role', 'consumption', 'usance', 'utilise', 'employment', 'function', 'economic_consumption', 'use_of_goods_and_services', 'manipulation', 'habituate', 'use', 'uses'],
    },
    {
        'intent': 'warnings',
        'patterns': 
            ["What are the warnings for _?", "What should I be aware of when taking _?", "What are the precautions for _?", "Are there any warnings for _?", "What should I know before taking _?", "What are the risks of taking _?", "What should I avoid when taking _?", "Are there any safety concerns with _?", "What are the danger signs when using _?", "What safety information should I know about _?", "What warnings come with _?", "What precautions should I take with _?", "What are the contraindications for _?", "What are the safety warnings for _?", "Are there any special warnings for _?"],
        'keywords':
            ['warning', 'monition', 'admonish', 'admonition', 'warn', 'monish', 'discourage', 'word_of_advice', 'warnings']
    },
    {
        'intent': 'dosage',
        'patterns':
            ["What is the dosage of _?", "How much _ should I take?", "What is the recommended dose of _?", "What dosage should be taken for _?", "How many milligrams of _ should I take?", "How often should I take _?", "Can you tell me the dosage of _?", "What is the prescribed dosage for _?", "What amount of _ is safe to take?", "How much _ is recommended?", "What is the daily dose of _?", "What is the standard dosage of _?", "How much _ should I take daily?", "What is the correct dosage of _?", "What is the appropriate dosage of _?", "What is the usual dose of _?"],
        'keywords':
            ['dosage', 'dose']
    },
    {
        'intent': 'side-effects',
        'patterns':
            ["What are the side effects of _?", "Does _ have any side effects?", "What adverse effects can _ cause?", "Are there any side effects of _?", "What should I watch out for when taking _?", "What are the common side effects of _?", "Can _ cause any side effects?", "What negative effects does _ have?", "Are there any adverse reactions to _?", "What are the potential side effects of _?", "What side effects should I expect from _?", "What are the known side effects of _?", "Does _ have any negative side effects?", "What harmful effects can _ cause?", "Are there any dangerous side effects of _?"],
        'keywords':
            ['outcome', 'gist', 'impression', 'essence', 'set_up', 'effect', 'consequence', 'core', 'result', 'upshot', 'effectuate', 'effects', 'force', 'event', 'issue', 'personal_effects', 'burden']
    },
]

intent_keywords = ['use', 'uses', 'dosage', 'dose', 'side', 'effects', 'side-effects', 'warnings', 'danger']

# connect with database
def connect_db():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["Chatbot_Data"]
    collection = db['medicine_data']
    
    return collection

# inserting data 
def insert_medicine_data(keyword, data):
    db_collection = connect_db()
    result = db_collection.insert_one({keyword : data})

    if result:
        return "Data inserted successfully in database :)"
    else:
        return "Error inserting data :("
    
# find data
def find_medicine_data(keyword):
    db_collection = connect_db()
    
    query = { f"{keyword}.medicine": keyword }
    result = db_collection.find_one(query)
    
    if result:
        # return "Data available in database :)"
        return result[keyword] 
    # return f"No data available of {keyword} :("
    return None

# medicine data extractor
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

def find_best_match(user_input):
    
    best_intent = None
    best_similarity = 0
    
    augmented_patterns = generate_augmented_patterns(user_input)
    
    for item in intent_data:
        for patterns in item['patterns']:
            for augmented_pattern in augmented_patterns:
                aug_pattern_doc = nlp(augmented_pattern)
                similarity = nlp(patterns).similarity(aug_pattern_doc)
                
                # print(f'pattern_doc : {aug_pattern_doc}')
                # print(f'augmented_pattern : {patterns}')
                # print(f'similarity : {similarity}')

                if similarity > best_similarity:
                    best_similarity = similarity
                    best_intent = item['intent']

    return best_intent, best_similarity

def get_response(user_input):

    intent, similarity = find_best_match(user_input)
    print(f'intent : {intent}, similarity : {similarity}')

    if intent and similarity > 0.7: 
        keyword = get_keywords(user_input)
        # print('keyword : ', keyword)

        for key in keyword:
            normalized_key = key.strip().lower()
            
            # skipping the intent keywords
            if normalized_key in intent_keywords:
                # print(f'Key {normalized_key} is an intent keyword or present in the intent so skipped')
                continue
                
            # if normalized_key in medicine_data.keys():
            medicine_data = find_medicine_data(normalized_key)
            if medicine_data:
                # print(f'Key {normalized_key} found in medicine_data')
                # if intent in medicine_data[normalized_key]:
                return random.choice(medicine_data[intent])

            else:
            # Run scraping script if data not found
                # print(f'Fetching new data for key : {normalized_key}')
                scraped_data = search_med(normalized_key)
                
                if scraped_data:
                    # medicine_data[normalized_key] = scraped_data
                    # insert_medicine_data(normalized_key, scraped_data)
                    # print('Data successfully fetch...')
                    # print('Updated medicine data : ', medicine_data)
                    
                    medicine_data = find_medicine_data(normalized_key)
                    if medicine_data:
                        num_choices = random.randint(2, 3)
                        return random.sample(medicine_data[intent], num_choices)
                    
                else:
                    return "Sorry, I couldn't find any information on that."
                
    return "Sorry, I don't have information on that. Let me try to fetch it for you."