from pymongo import MongoClient
import config


async def get_connection():
    # print(config.MONGO_CONN_STR)
    client = MongoClient(config.MONGO_CONNECTION_URI)
    db = client[config.DB_NAME]
    return db
