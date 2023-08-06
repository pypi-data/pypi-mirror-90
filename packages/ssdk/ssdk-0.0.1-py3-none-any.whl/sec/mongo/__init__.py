import os

from pymongo import MongoClient


def client():
    return MongoClient(os.environ.get('SEC__MONGO_URL'))
