import pymongo
import pandas as pd  
import numpy as np  
import json

client = pymongo.MongoClient("mongodb+srv://ShraddhasCluster:shraddha123@cluster0.lmyl9ac.mongodb.net/?retryWrites=true&w=majority")

DATABASE_NAME ="BANK_LEADS"
COLLECTION_NAME ="LEADS"

if __name__=="__main__":
    
    df = pd.read_csv(r"/config/workspace/bank-additional-full.csv", sep =";")
    print(f"Rows and columns: {df.shape}")

    #Convert dataframe to json
    df.reset_index(drop=True, inplace=True)

    #First Transpose your DataFrame
    json_record = list(json.loads(df.T.to_json()).values())

    #printing single record
    print(json_record[0])

    #Insert converted record to MongoDB
    client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)

    

