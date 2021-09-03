"""Provides mongodb interface for objects"""
import pymongo as pm
from logger import logger


class MongoConnection:
    """mongodb connection"""

    def __init__(
        self, host="127.0.0.1", port=27017, db_name=None, related_collections=[]
    ):
        """
        set default host to not local computer
        """
        self.host = host
        self.port = port
        self.connection = None
        self.db = None
        self._db_name = db_name
        self._collections = related_collections
        for col in related_collections:
            setattr(self, f"{col}", None)

    def __enter__(self):
        """
        provide context manager for connection
        """
        self.connection = pm.MongoClient(self.host, self.port)
        self.db = self.connection[self._db_name]
        for col in self._collections:
            setattr(self, f"{col}", self.db[col])

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db = None
        for col in self._collections:
            setattr(self, f"{col}", None)
        self.connection.close()

    def connect(self):
        """
        non context manager for connection
        """

        self.__enter__()
        return True

    def close(self, *args):
        """
        non context manager to close connection
        """
        self.connection.close()
        return True

    def _verify_docs(self, collection, **kwargs):
        """verify that a doc exists meeting each criteria"""
        with self:
            col = self.db[collection]
            for kw, arg in kwargs.items():
                query = {kw: arg}
                record = col.find_one(query)
                if not record:
                    return False
        return True

    @staticmethod
    def _create_dict(update=True, **kwargs):
        """create an update statement from given kwargs"""
        if update:
            return {
                "$set": {kw: arg for (kw, arg) in kwargs.items() if arg is not None}
            }
        return {kw: arg for (kw, arg) in kwargs.items() if arg is not None}


mongo = MongoConnection(
    db_name="Realms_MUD", related_collections=["Players", "Items", "Rooms", "Npcs"]
)
