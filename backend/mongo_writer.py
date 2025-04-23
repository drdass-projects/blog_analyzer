from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client[os.getenv("MONGODB_DB")]
collection = db[os.getenv("MONGODB_COLLECTION")]

def save_to_mongo(keyword, blogs):
    document = {
        "keyword": keyword,
        "analyzed_at": datetime.utcnow(),
        "total_blogs": len(blogs),
        "blogs": blogs
    }

    # Upsert (update if exists, insert if not)
    collection.update_one(
        {"keyword": keyword},
        {"$set": document},
        upsert=True
    )
