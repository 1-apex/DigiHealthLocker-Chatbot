import spacy

# def handle_user_query(user_message):
nlp = spacy.load("en_core_web_lg")


medicine_data = {
    'aspirin': {
        'uses': ["Aspirin is used to treat pain, and reduce fever or inflammation. It is sometimes used to treat or prevent heart attacks, strokes, and chest pain (angina)."],
        'warnings': ["Aspirin may cause stomach or intestinal bleeding, which can be fatal."],
        'dosage': ["The usual dose for adults is one or two tablets every four hours as needed."],
        'side-effects': ["Common side effects include upset stomach and heartburn."]
    },
    # Add more medicines as needed
}

# Predefined intents and responses
intent_patterns = [
    {
        'intent': 'information',
        'patterns': ['Tell me use about aspirin', 'What is aspirin used for?'],
        'keywords': 'aspirin',
        'response': [
            'Aspirin is a salicylate (sa-LIS-il-ate). It works by reducing substances in the body that cause pain, fever, and inflammation.',
            'Aspirin is used to treat pain, and reduce fever or inflammation. It is sometimes used to treat or prevent heart attacks, strokes, and chest pain (angina).'
        ]
    },
    # Add more intents and patterns as needed
]

def process_user_input(user_input):
    doc = nlp(user_input)
    return doc

def find_best_match(user_input, intent_patterns):
    user_doc = process_user_input(user_input)
    best_match = None
    best_similarity = 0

    for pattern in intent_patterns:
        for p in pattern['patterns']:
            pattern_doc = nlp(p)
            print('pattern_doc : ', pattern_doc)
            similarity = user_doc.similarity(pattern_doc)
            print('similarity : ', similarity)
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
    return "Sorry, I don't have information on that. Let me try to fetch it for you."

# Example usage
user_input = "Tell me about the uses of aspirin"
response = get_response(user_input, intent_patterns, medicine_data)
print("Response:", response)

    