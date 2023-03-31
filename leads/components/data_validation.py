import pandas as pd  
import numpy as np  
from leads.logger import logging
from leads.exception import LeadException
from leads import config
from leads import utils
from leads.entity import config_entity,artifact_entity
from leads.components import data_ingestion
from typing import Optional
from leads.config import TARGET_COLUMN
from scipy.stats import ks_2samp

class DataValidation:

    def __init__(self, data_validation_config:config_entity.DataValidationConfig,
                    data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*20} Data Validation {'>>'*20}")
            self.data_validation_config= data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.validation_error=dict()
        except Exception as e:
            raise LeadException(e, sys)
    
    def drop_missing_values_columns(self, df:pd.DataFrame,report_key_name:str)->Optional[pd.DataFrame]:
        try:
            threshold = self.data_validation_config.missing_threshold
            null_report = df.isna().sum()/df.shape[0]
            drop_column_names = null_report[null_report>threshold].index
            self.validation_error[report_key_name]=list(drop_column_names)
            df.drop(list(drop_column_names), axis=1, inplace=True)

            if len(df.columns==0):
               return None
            return df
        except Exception as e:
            raise LeadException(e, sys)
    
    def is_required_columns_exists(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str)->bool:
        try:
            base_columns = base_column.df
            current_colums = current_column.df
            
            missing_columns = []
            for base_column in base_columns:
                if base_column not in current_columns:
                    missing_columns.append(base_column)

            if len(missing_columns)>0:
                self.validation_error[report_key_name]=missing_columns
                return False
            return True

        except Exception as e:
            raise LeadException(e, sys)
    
    def data_drift(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str):
        try:
            
            base_columns = base_df.columns
            current_columns  = current_df.columns

            for base_column in base_columns:
                base_data, current_data = base_df[base_column],current_df[current_column]
                same_distribution = ks_2samp(base_data,current_data)

            if same_distribution.pvalue>0.05:
                drift_report[base_column] = {
                    "pvalues": float(same_distribution.pvalue),
                    "same_distribution":True
                }
            else:
                drift_report[base_column]={
                    "pvalues":float(same_distribution.pvalue),
                    "same_distribution":False
                }

        except Exception as e:
            raise LeadException(e,sys)

    def initiate_data_validation(self,)->artifact_entity.DataValidationArtifact:
        try:
            base_df = pd.read_csv(self.data_validation_config.base_file_path)
            


        except Exception as e:
            raise LeadException(e, sys)
