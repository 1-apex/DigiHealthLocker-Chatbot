import pymongo

# connect with  mongodb compass 
client = pymongo.MongoClient("mongodb://localhost:27017/")

# list the databases 
# dblist = client.list_database_names()
# print(dblist)

# list the collections present in the database
# db = client["User_DB"]
# dbconnections = db.list_collection_names()
# print(dbconnections)

# inserting the data
db = client["Chatbot_Data"]
collection = db['data']


message = {
    'intent' : ['information'],
    'pattern' : ['Tell me use about aspirin medicine', 'Aspirin medicine information'],
    'keywords' : ['aspirin'],
    'response' : [
        'Aspirin is a salicylate (sa-LIS-il-ate). It works by reducing substances in the body that cause pain, fever, and inflammation.',
        'Aspirin is used to treat pain, and reduce fever or inflammation. It is sometimes used to treat or prevent heart attacks, strokes, and chest pain (angina).'
        ]
}

# status = collection.insert_one(message)
import spacy

# Load the pre-trained model
nlp = spacy.load('en_core_web_lg')

def identify_nouns(sentence):
    # Process the sentence using spaCy
    doc = nlp(sentence)
    
    nouns = []
    # Iterate over the tokens in the processed document
    for token in doc:
        if token.pos_ == "NOUN":
            nouns.append(token.text)
    
    return nouns

# Example usage
sentence = "aspirin"
nouns = identify_nouns(sentence)
print("Nouns:", nouns)