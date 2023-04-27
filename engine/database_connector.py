import pymongo
import json
from bson import json_util
from engine.discord_notification import discord
from dotenv import load_dotenv
import os


def connect_to_db():
    load_dotenv()
    try:
        conn_str = os.environ["DB_CONNECTION_URI"]
        client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
        server_info = client.server_info()
        server_info = client.address
        print(f"Connected to: {server_info[0]}")
        # Database name
        global database
        database = client[os.environ["DB_NAME"]]
        return True
    except:
        return False


def write_to_db(data, collection):
    collection = database[collection]
    try:
        collection.insert_one(data)
        discord(data)
    except Exception as e:
        print(data)
        print(f"Error: {e}")


def query_db(data, collection):
    collection = database[collection]
    return collection.find_one(data)


def dump_db(collection):
    collection = database[collection]
    return collection.find()


def dump_as_json(collection):
    collection = database[collection]
    documents = list(collection.find())
    json_data = json_util.dumps(documents, indent=4)
    return json.loads(json_data)
