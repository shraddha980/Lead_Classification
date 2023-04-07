import os
import sys
from leads.logger import logging
from leads.exception import LeadException
import pandas as pd
from leads.config import mongo_client
import pymongo
import dill
import pymongo
import numpy as np

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

def save_object(file_path:str, obj:object)-> None:
    try:
            logging.info("Enter the save object method of utils")
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "wb") as file_obj:
                dill.dump(obj,file_obj)
            logging.info("Exited the save object method of utils")
    except Exception as e:
        raise LeadException(e, sys)
    
def load_object(file_path:str, obj:object)-> None:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file : {file_path} is not exsts")
            with open(file_path, "rb") as file_obj:
                return dill.load(file_obj)
    except Exception as e:
            raise LeadException(e, sys)

def save_numpy_array_data(file_path: str, array = np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise LeadException(e, sys)

def load_numpy_array_data(file_path:str)-> np.array:
    try:
        with open(file_path, "rb") as file_obj:
         return np.load(file_obj)
    except Exception as e:
        raise LeadException(e, sys)



def convert_columns_float(df:pd.DataFrame, exclude_columns:list)-> pd.DataFrame:
    try:
        for column in df.columns:
            if column not in exclude_columns:
                df[column]=df[column].astype('float')
        return df 
    except Exception as e:
        raise LeadException(e, sys)

def write_yaml(file_path, data:dict):
    try:
       file_dir = os.path.dirname(file_path)
       os.makedirs(file_dir,exist_ok=True)
       with open(file_path,"w") as file_writer:
         yaml.dump(data, file_writer)
    except Exception as e:
        raise LeadException(e,sys)
     
    