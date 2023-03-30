import os
import sys
from leads.logger import logging
from leads.exception import LeadException


def get_collection_as_dataframe(database_name:str, collection_name:str)->pd.DataFrame:
    try:
       logging.info("Getting collection name and database name")
       df = mongo_client

    except Exception as e:
        raise LeadException(e,sys)
    