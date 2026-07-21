import pandas as pd

from database.mongodb import MongoDBConnection


class DataLoader:
    """
    Loads data from MongoDB Atlas into a Pandas DataFrame.
    """

    def __init__(self):
        """
        Create a MongoDB connection.
        """
        self.db = MongoDBConnection()

    def load_data(self):
        """
        Load all documents from the MongoDB collection.

        Returns
        -------
        pandas.DataFrame
            DataFrame containing all documents.
        """

        collection = self.db.get_collection()

        documents = list(
            collection.find(
                {},
                {"_id": 0}
            )
        )

        dataframe = pd.DataFrame(documents)

        return dataframe

    def close_connection(self):
        """
        Close MongoDB connection.
        """
        self.db.close_connection()