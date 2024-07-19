import spacy
nlp = spacy.load("en_core_web_lg")

def get_keywords(user_input):
    doc = nlp(user_input)
    
    keywords = set()
    
    for word in doc:
        # print(f'{word} : {word.tag_}')
        if word.tag_ in ['NNP', 'NNS', 'NN']:
            keywords.add(word.text)
 
    return list(keywords)

# sentence = "tell me more uses of it"
# keywords = get_keywords(sentence)
# print(keywords)