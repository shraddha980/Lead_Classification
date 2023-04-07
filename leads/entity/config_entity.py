import os
import sys
from datetime import datetime
from leads.logger import logging
from leads.exception import LeadException

FILE_NAME = "bank-additional-full.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"
TRANSFORMER_OBJECT_FILE_NAME = "transformer.pkl"
TARGET_ENCODER_OBJECT_FILE_NAME = "target_encoder.pkl"
MODEL_FILE_NAME = "model.pkl"

class TrainingPipelineConfig:
    
    def __init__(self):
        try:
            self.artifact_dir = os.path.join(os.getcwd(),"artifact", f"{datetime.now().strftime('%d%m%Y__%H%M%S')}")
        except exception as e:
            raise LeadException(e,sys)


class DataIngestionConfig:
       
       def __init__(self,training_pipeline_config:TrainingPipelineConfig):
           try:
              self.database_name="BANK_LEADS"
              self.collection_name="LEADS"
              self.data_ingestion_dir=os.path.join(training_pipeline_config.artifact_dir,"data_ingestion")
              self.feature_store_file_path=os.path.join(self.data_ingestion_dir,"feature_store", FILE_NAME)
              self.train_file_path=os.path.join(self.data_ingestion_dir,"dataset", TRAIN_FILE_NAME)
              self.test_file_path=os.path.join(self.data_ingestion_dir,"dataset", TEST_FILE_NAME)
              self.test_size=0.2
           except Exception as e:  
                raise LeadException(e,sys)

       def to_dict(self,)->dict:
            try:
                return self.__dict__
            except Exception as e:
                raise LeadException(e, sys)

class DataValidationConfig:
      
      def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_validation_dir = os.path.join(training_pipeline_config.artifact_dir, "data_validation")
        self.report_file_path = os.path.join(data_validation_dir,"report.yaml")
        self.missing_threshold:float = 0.7
        self.base_file_path = os.path.join("bank-additional-full.csv")

class DataTransformationConfig:
    
    def __init__(self,train_pipeline_config:TrainingPipelineConfig):
        self.data_transformation_dir = os.path.join(training_pipeline_config.artifact_dir,"data_transformation")
        self.transformed_object_path = os.path.join(data_transformation_dir, "transformer", TRANSFORMED_OBJECT_FILE_NAME)
        self.transformed_train_path = os.path.join(data_transformation_dir, "transformed", TRAIN_FILE_NAME.replace("csv","npz"))
        self.transformed_test_path = os.path.join(data_transformation_dir,"transformed",TEST_FILE_NAME.replace("csv","npz"))
        self.target_encoder_path = os.path.join(data_transformation_dir,"target_encoder",TARGET_ENCODER_FILE_NAME)

class ModelTrainerConfig:
    
    def __init__(self,train_pipeline_config:TrainingPipelineConfig):
        self.model_trainer = os.path.join(train_pipeline_config.artifact_dir,"model_trainer")
        self.model_path = os.path.join(self.model_trainer, "model", MODEL_FILE_NAME)
        self.expected_score = 0.5
        self.overfitting_threshold = 0.1
        
class ModelEvaluationonfig:
    
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.change_threshold = 0.01   

class ModelPusherConfig:
    
        def __init__(self,training_pipeline_config:TrainingPipelineConfig):
          self.model_pusher_dir = os.path.join(training_pipeline_config.artifact_dir , "model_pusher")
          self.saved_model_dir = os.path.join("saved_models")
          self.pusher_model_dir = os.path.join(self.model_pusher_dir,"saved_models")
          self.pusher_model_path = os.path.join(self.pusher_model_dir,MODEL_FILE_NAME)
          self.pusher_transformer_path = os.path.join(self.pusher_model_dir,TRANSFORMER_OBJECT_FILE_NAME)
          self.pusher_target_encoder_path = os.path.join(self.pusher_model_dir,TARGET_ENCODER_OBJECT_FILE_NAME)

