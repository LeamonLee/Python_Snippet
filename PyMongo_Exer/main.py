#import Pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

# conn = MongoClient("10.101.100.97", 27017)
conn = MongoClient("localhost", 27017)

db = conn["core"]
# db = conn.core                                # This way also works

collection = db["last_value"]

print("Connecting to the MongoDB database...", conn)

# print(collection.stats)

print("Showing collections...")
for collects in collection.find():
    print(collects)

print("Showing collections...")
cursor = collection.find({})
for data in cursor:
    print(data)

print('='*50)

def get_db(strHost, nPort, strDB):
    # Create connection
    client = MongoClient(strHost, nPort)
    retDB = client[strDB]
    return retDB


def get_collection(db, strCollectionName):
    coll = db[strCollectionName]
    print(db.list_collection_names())
    return coll


def insert_one_doc(db, strCollectionName, objDocument):
    coll = db[strCollectionName]
    information_id = coll.insert(objDocument)
    print(information_id)


def insert_multi_docs(db, strCollectionName, arrDocuments):
    coll = db[strCollectionName]
    information_id = coll.insert(arrDocuments)
    print(information_id)


def get_one_doc(db, strCollectionName, objCondition):
    coll = db[strCollectionName]
    print(coll.find_one(objCondition))


# ret_Coll = get_collection(db, "last_value")

