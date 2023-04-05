import os
import sys
from leads.entity import artifact_entity,config_entity
from leads.config import TARGET_COLUMN
from leads.components import data_ingestion,data_transformation,data_validation
from leads.logger import logging
from leads.exception import LeadException
from sklearn.metrics import f1_score
from xgboost import XGBClassifier

class ModelTrainer:

    def __init__(self,model_trainer_config:config_entity.ModelTrainerConfig,
                      data_transformation_artifact:artifact_entity.DataTransformationArtifact):
        try:
            logging.info(f"{'>>'*20} Model Trainer {'>>'*20}")
            self.model_trainer_config:model_trainer_config
            self.data_transformation_artifact: data_transformation_artifact
        except Exception as e:
            raise LeadException(e,sys)

    def train_model(self,x,y):
        try:
            xgb_clf = XGBClassifier()
            xgb_clf.fit(x,y)
            return xgb_clf
        except Exception as e:
            raise LeadException(e, sys)
    
    def initiate_model_trainer(self,)-> artifact_entity.ModelTrainerArtifact:


    