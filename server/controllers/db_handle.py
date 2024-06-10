import pymongo

# connecting with the medicine_data
def connect_db():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["Chatbot_Data"]
    collection = db['medicine_data']
    
    return collection

# inserting data 
def insert_medicine_data(keyword, data):
    db_collection = connect_db()
    result = db_collection.insert_one({keyword : data})

    if result:
        return "Data inserted successfully in database :)"
    else:
        return "Error inserting data :("
    
# find data
def find_medicine_data(keyword):
    db_collection = connect_db()
    
    query = { f"{keyword}.medicine": keyword }
    result = db_collection.find_one(query)
    
    if result:
        # return "Data available in database :)"
        return result[keyword] 
    # return f"No data available of {keyword} :("
    return None