import pymongo

# connecting with the medicine_data
def connect_db():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["Chatbot_Data"]
    collection = db['data']
    
    return collection

# inserting data (keyword == medicine)
def insert_medicine_data(keyword, data):
    db_collection = connect_db()
    x = db_collection.insert_one({keyword : data})
    if x:
        return "Data inserted successfully in database"
    else:
        return "Error inserting data :("
    
# find data (keyword == medicine)
def find_medicine_data(keyword):
    db_collection = connect_db()
    
    query = { f"{keyword}.medicine": keyword }
    # Query the collection
    x = db_collection.find_one(query)
    # print(x)
    if x:
        return "Data available in database"
    else:
        return f"No data available of {keyword} :("
    
print(find_medicine_data('paracetamol'))