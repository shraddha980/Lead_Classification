import pandas 
import numpy as np  
import os
import sys
from leads.logger import logging
from leads.exception import LeadException
from leads import utils
from leads.entity import config_entity
from leads.entity.config_entity import DataIngestionConfig
from leads.entity import artifact_entity
from leads.components import data_ingestion
from leads.components.data_ingestion import DataIngestion

if __name__ == "__main__":
    try:
        training_pipeline_config = config_entity.TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        print(data_ingestion_config.to_dict())
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)

    except Exception as e:
         print(e)