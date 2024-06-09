from nltk.corpus import wordnet

# Function to find synonyms of a word
def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return list(synonyms)

# Get synonyms of the word
# word = "effects"
# synonyms = get_synonyms(word)
# print(synonyms)
