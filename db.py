from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(verbose=True, override=True)

try: 
    db = MongoClient(os.environ["MONGO_URI"])["sudoku"]
    print("MONGODB CONNECTION IS SUCCESSFUL!")
except KeyError:
    raise Exception("You haven't configured your MONGO_URI!")

def refresh_client():
    global db
    db = MongoClient(os.environ["MONGO_URI"])["sudoku"]
    print("refresh_client()")

def predictions_insert(transaction_id, model_version, digit, probability, \
    public_url=None, label=None, label_user=None, label_dttm=None):
    doc = {"transaction_id": transaction_id,
            "model_version": model_version,
            "digit" : digit,
            "probability": probability,
            "datetime": datetime.utcnow(),
            "public_url": public_url,
            "label": label,
            "label_user": label_user,
            "label_dttm": label_dttm}

    oid = db.predictions.insert_one(doc)
    return oid

def predictions_update_public_url(transaction_id, public_url):
    db.predictions.update_one(filter={"transaction_id": transaction_id}, \
        update={"$set": {"public_url": public_url}})

def predictions_update_label(transaction_id, label):
    db.predictions.update_one(filter={"transaction_id": transaction_id}, \
        update={"$set": {"label": label, "label_dttm": datetime.utcnow()}} )

def predictions_get_random_unlabeled():
    aggr = list(db.predictions.aggregate([
        { 
            "$match": { 
                "label": None ,
                "public_url": { "$ne": None }
            }
        },
        { 
            "$sample": { 
                "size": 1 
            } 
        }
        ]))
    if len(aggr) > 0:
        return aggr[0]
    else:
        None
    # return db.predictions.find_one(filter={"label": None})

def predictions_get(transaction_id):
    return db.predictions.find_one(filter={"transaction_id": transaction_id})


