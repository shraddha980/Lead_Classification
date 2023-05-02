import os
import sys
import pandas as pd
import numpy as np
from leads.utils import load_object
from leads.logger import logging
from leads.exception import LeadException
from leads.entity import config_entity, artifact_entity
from leads.entity.artifact_entity import DataIngestionArtifact,DataTransformationArtifact,DataValidationArtifact, ModelTrainerArtifact
from leads.components import data_ingestion, data_transformation, data_validation
from leads.config import TARGET_COLUMN
from sklearn.metrics import f1_score
from leads.predictor import ModelResolver

class ModelEvaluation():

    def __init__(self,
                model_eval_config:config_entity.ModelEvaluationonfig,
                data_ingestion_artifact:artifact_entity.DataIngestionArtifact,
                data_transformation_artifact:artifact_entity.DataTransformationArtifact,
                model_trainer_artifact:artifact_entity.ModelTrainerArtifact,
               ):
      try:
        logging.info(f"{'>>'*20} Model Evaluation {'<<'*20}")
        self.model_eval_config = model_eval_config
        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_artifact = model_trainer_artifact
        self.model_resolver = ModelResolver()
      except Exception as e:
        raise LeadException(e, sys)

    def initiate_model_evaluation(self)-> artifact_entity.ModelEvaluationArtifact:
        try:
          '''
          If Saved Model Folder has model we will compare which
          model is best trained or model from the saved folder
           '''

          logging.info("If saved model has model we will compare which model is best trained or \
                         model from saved folder")
          latest_dir_path = self.model_resolver.get_latest_dir_path()
          if latest_dir_path==None:
             model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True, improved_accuracy=None)
             logging.info(f"Model Evaluation Artifact : {model_eval_artifact}")
             return model_eval_artifact

          logging.info("Finding location of Transformer Model and Target Encoder")
          transformer_path = self.model_resolver.get_latest_transformer_path()
          model_path = self.model_resolver.get_latest_model_path()
          target_encoder_path = self.model_resolver.get_latest_target_encoder_path()

          logging.info("Previous Trained objects of Model Transformer, Encoder and Model")
          transformer = load_object(file_path = transformer_path)
          model = load_object(file_path = model_path)
          target_encoder = load_object(file_path = target_encoder_path)
          logging.info(f"Target_Encoder = : {target_encoder}")

          logging.info("Currently trained model objects")
          current_transformer= load_object(file_path= self.data_transformation_artifact.transform_object_path)
          current_model= load_object(file_path=self.model_trainer_artifact.model_path)
          current_target_encoder=load_object(file_path=self.data_transformation_artifact.target_encoder_path)

          test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
          target_df = test_df["y"]
          y_true = target_encoder.fit_transform(target_df)

          input_feature_name = list(transformer.feature_names_in_)
          input_arr = transformer.transform(test_df[input_feature_name])
          y_pred = model.predict(input_arr)
          print(f"Prediction using previous model : {target_encoder.inverse_transform(y_pred[:5])}")
          previous_model_score = f1_score(y_true=y_true, y_pred = y_pred)
          logging.info(f"Accuracy using previous trained model : {previous_model_score}")

          input_feature_name = list(current_transformer.feature_names_in)
          input_arr = current_transformer.transform(test_df[input_feature_name])
          y_pred = current_model.predict(input_arr)

          y_true = current_target_encoder.transform(target_df)
          current_model_score = f1_score(y_true=y_true, y_pred = y_pred)

          logging.info(f"Accuracy using current trained model : {current_model_score}")

          if current_model_score <= previous_model_score:
            logging.info(f"Current trained model is not better than previous trained model")
            raise Exception(f"Current trained model is not better than previous trained model")

          model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True, improved_accuracy=current_model_score-previous_model_score)
          logging.info(f"Model eval artifact : {model_eval_artifact}")
          return model_eval_artifact
        except Exception as e:
          raise LeadException(e, sys)

        