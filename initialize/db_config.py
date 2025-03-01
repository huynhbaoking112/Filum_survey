import mongoengine
import logging

def connection_mongodb():
    try:
        mongoengine.connect(
            host="mongodb+srv://huynhbaoking:kingking@cluster0.x8auz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        )
        logging.info("MongoDB connection established successfully.")
    except Exception as e:
        logging.error(f"Error connecting to MongoDB: {e}")