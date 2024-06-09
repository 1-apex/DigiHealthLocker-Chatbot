from synonyms import *
import spacy
nlp = spacy.load("en_core_web_lg")

# Function to generate patterns from the user input
def generate_augmented_patterns(user_input):
    augmented_patterns = set()
    doc = nlp(user_input)
    count = 0
    for token in doc:
        synonyms = get_synonyms(token.text)
        for synonym in synonyms:
            augmented_pattern = user_input.replace(token.text, synonym)
            augmented_patterns.add(augmented_pattern)
            count += 1
            if count >= 5:
                return list(augmented_patterns)
    return list(augmented_patterns)