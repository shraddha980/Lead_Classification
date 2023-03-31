import os
import sys
from leads.logger import logging
from leads.exception import LeadException
import pandas as pd
from leads.config import mongo_client
import pymongo
import dill
import pymongo

client = pymongo.MongoClient("mongodb+srv://BackOrderPropagation:shraddha123@cluster0.y1c9hs5.mongodb.net/?retryWrites=true&w=majority")
DATABASE_NAME ="BANK_LEADS"
COLLECTION_NAME ="LEADS"

def get_collection_as_dataframe(database_name:str,collection_name:str)->pd.DataFrame:
    """
    Description: This function return collection as dataframe
    =========================================================
    Params:
    database_name: database name
    collection_name: collection name
    =========================================================
    return Pandas dataframe of a collection
    """
    try:
        logging.info(f"Reading data from database: {database_name} and collection: {collection_name}")
        
        df = pd.DataFrame(list(client[DATABASE_NAME][COLLECTION_NAME].find()))
        logging.info(f"Found columns: {df.columns}")
        if "_id" in df.columns:
            logging.info(f"Dropping column: _id ")
            df = df.drop("_id",axis=1)
        logging.info(f"Row and columns in df: {df.shape}")
        return df
    except Exception as e:
        raise LeadException(e, sys)
    