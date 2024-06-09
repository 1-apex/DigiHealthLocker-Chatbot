from modules.synonyms import get_synonyms
import spacy
nlp = spacy.load("en_core_web_lg")

# Function to generate patterns from the user input
def generate_augmented_patterns(user_input):
    augmented_patterns = set()
    doc = nlp(user_input)
    for token in doc:
        synonyms = get_synonyms(token.text)
        for synonym in synonyms:
            augmented_pattern = user_input.replace(token.text, synonym)
            augmented_patterns.add(augmented_pattern)
    return list(augmented_patterns)