import os

from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()


class MongoDBConnection:
    """
    Handles MongoDB Atlas connection.
    """

    def __init__(self):

        self.client = MongoClient(
            os.getenv("MONGODB_URI")
        )

        self.database = self.client[
            os.getenv("DATABASE_NAME")
        ]

    def get_collection(self):

        return self.database[
            os.getenv("COLLECTION_NAME")
        ]

    def close_connection(self):

        self.client.close()