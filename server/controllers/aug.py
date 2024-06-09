from nltk.corpus import wordnet
import spacy
import random
# from .medicine_data_extractor import search_med
from ..modules.augmented_data_generation import generate_augmented_patterns
from modules.keywords import get_keywords

# Load spaCy model
nlp = spacy.load("en_core_web_lg")

# def get_synonyms(word):
#     synonyms = set()
#     for syn in wordnet.synsets(word):
#         for lemma in syn.lemmas():
#             synonyms.add(lemma.name().replace('_', ' '))
#     return list(synonyms)

# def generate_augmented_patterns(user_input):
#     augmented_patterns = set()
#     doc = nlp(user_input)
#     for token in doc:
#         synonyms = get_synonyms(token.text)
#         for synonym in synonyms:
#             augmented_pattern = user_input.replace(token.text, synonym)
#             augmented_patterns.add(augmented_pattern)
#     return list(augmented_patterns)

def find_best_match(user_input, database):
    
    best_intent = None
    best_similarity = 0
    
    augmented_patterns = generate_augmented_patterns(user_input)
    
    for item in database:
        for patterns in item['patterns']:
            for augmented_pattern in augmented_patterns:
                aug_pattern_doc = nlp(augmented_pattern)
                similarity = patterns.similarity(aug_pattern_doc)
                
                print(f'pattern_doc : {aug_pattern_doc}')
                print(f'augmented_pattern : {patterns}')
                print(f'similarity : {similarity}')

                if similarity > best_similarity:
                    best_similarity = similarity
                    best_intent = item['intent']

    return best_intent, best_similarity

def get_response(user_input, database, medicine_data):
    intent, similarity = find_best_match(user_input, database)
    print(f'intent : {intent}, similarity : {similarity}')
    if intent and similarity > 0.7: 
        keyword = get_keywords(user_input)
        print('keyword : ', keyword)
        if keyword in medicine_data:
            if medicine_data[keyword][intent]:
                pass
            else:
                return random.choice(medicine_data[keyword][intent]) 
        else:
            # Run scraping script if data not found
            
            # scraped_data = search_med(keyword)
            # if scraped_data:
            #     medicine_data[keyword] = scraped_data
            #     return scraped_data['uses'][0]  # Example: Fetch 'uses' information from scraped data
            # else:
            return "Sorry, I couldn't find any information on that."
    return "Sorry, I don't have information on that. Let me try to fetch it for you."

# Example usage
database = [
    {
        'intent': 'uses',
        'patterns': ['What is the use of ?', 'Uses of ', 'Application of ', 'Usage of medicine like '],
        'keywords': ['purpose', 'habit', 'expend', 'utilisation', 'utilization', 'apply', 'employ', 'practice', 'usage', 'enjoyment', 'exercise', 'utilize', 'role', 'consumption', 'usance', 'utilise', 'employment', 'function', 'economic_consumption', 'use_of_goods_and_services', 'manipulation', 'habituate', 'use'],
    },
    # Add more intents and patterns as needed
]

medicine_data = {
    'aspirin': {
        'uses': ["Aspirin is used to treat pain, and reduce fever or inflammation. It is sometimes used to treat or prevent heart attacks, strokes, and chest pain (angina)."],
        'warnings': ["Aspirin may cause stomach or intestinal bleeding, which can be fatal."],
        'dosage': ["The usual dose for adults is one or two tablets every four hours as needed."],
        'side-effects': ["Common side effects include upset stomach and heartburn."]
    },
    # Add more medicines as needed
}

user_input = "Tell me about the uses of aspirin"
response = get_response(user_input, database, medicine_data)
print("Response:", response)


