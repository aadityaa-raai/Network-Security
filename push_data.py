import os
import sys
import json

from dotenv import load_dotenv
load_dotenv()

mongodb_url=os.getenv("mongodb_url")

print(mongodb_url)

import certifi
ca=certifi.where()

import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

class NetworkDataExtract():
    def __init__(self):
        try:
            pass

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def cv_to_json_convertor(self,file_path):
        try:
            data=pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            records=list(json.loads(data.T.to_json()).values())
            return records

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def insert_data_to_mongodb(self,records,database,collection):
        try:
            self.records=records
            self.database=database
            self.collection=collection

            self.mongo_client=pymongo.MongoClient(mongodb_url)
            self.database=self.mongo_client[self.database]
            self.collection=self.database[self.collection]
            self.collection.insert_many(self.records)

            return len(self.records)
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)

if __name__=='__main__':
    file_path="Network_Data\\phisingData.csv"
    database='Aditya_DB'
    collection="NetworkData"
    network_obj=NetworkDataExtract()
    records=network_obj.cv_to_json_convertor(file_path)
    no_of_records=network_obj.insert_data_to_mongodb(records,database,collection)
    logging.info("Records uploaded")
    print(no_of_records)