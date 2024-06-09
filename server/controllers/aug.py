from nltk.corpus import wordnet
import spacy
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
# from .medicine_data_extractor import search_med

# Load spaCy model
nlp = spacy.load("en_core_web_lg")

def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().replace('_', ' '))
    return list(synonyms)

def generate_augmented_patterns(user_input):
    augmented_patterns = set()
    doc = nlp(user_input)
    for token in doc:
        synonyms = get_synonyms(token.text)
        for synonym in synonyms:
            augmented_pattern = user_input.replace(token.text, synonym)
            augmented_patterns.add(augmented_pattern)
    return list(augmented_patterns)

def process_user_input(user_input):
    doc = nlp(user_input)
    return doc

def find_best_match(user_input, intent_patterns):
    user_doc = process_user_input(user_input)
    print('user_doc : ', user_doc)
    print('user_input : ', user_input)
    best_match = None
    best_similarity = 0

    for pattern in intent_patterns:
        augmented_patterns = generate_augmented_patterns(user_input)
        print(f'Augmented_Patterns : {augmented_patterns}')
        for augmented_pattern in augmented_patterns:
            pattern_doc = nlp(augmented_pattern)
            similarity = user_doc.similarity(pattern_doc)
            # print('user_doc : ', user_doc)
            # print('pattern_doc : ', pattern_doc)
            # print('similarity : ', similarity)
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = pattern

    return best_match, best_similarity

def get_response(user_input, intent_patterns, medicine_data):
    match, similarity = find_best_match(user_input, intent_patterns)
    if match and similarity > 0.7:  # Threshold for similarity
        keyword = match['keywords']
        if keyword in medicine_data:
            return medicine_data[keyword]['uses'][0]  # Example: Fetch 'uses' information
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
intent_patterns = [
    {
        'intent': 'information',
        'patterns': ['Tell me about aspirin', 'What is aspirin used for?'],
        'keywords': 'aspirin',
        'response': [
            'Aspirin is a salicylate (sa-LIS-il-ate). It works by reducing substances in the body that cause pain, fever, and inflammation.',
            'Aspirin is used to treat pain, and reduce fever or inflammation. It is sometimes used to treat or prevent heart attacks, strokes, and chest pain (angina).'
        ]
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
response = get_response(user_input, intent_patterns, medicine_data)
print("Response:", response)


