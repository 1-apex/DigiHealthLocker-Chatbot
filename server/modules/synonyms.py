from nltk.corpus import wordnet

# Function to find synonyms of a word
def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return synonyms

# Get synonyms of the word "use"
word = "use"
synonyms = get_synonyms(word)
print(synonyms)
