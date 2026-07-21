import streamlit as st
from pymongo import MongoClient


class MongoDBConnection:

    def __init__(self):

        self.client = MongoClient(
            st.secrets["MONGODB_URI"]
        )

        self.database = self.client[
            st.secrets["DATABASE_NAME"]
        ]

    def get_collection(self):

        return self.database[
            st.secrets["COLLECTION_NAME"]
        ]

    def close_connection(self):

        self.client.close()