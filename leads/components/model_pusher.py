import pandas as pd   
import numpy as np  
from leads.logger import logging
from leads.exception import LeadException
from leads.entity import config_entity, artifact_entity
from leads.components import data_ingestion,data_transformation,data_validation, model_evaluation,model_pusher,model_trainer
import os
import sys
from leads import utils
from leads.predictor import ModelResolver
from leads.utils import load_object, save_object
from leads.entity.config_entity import ModelPusherConfig
from leads.entity.artifact_entity import ModelPusherArtifact
from leads.entity.artifact_entity import DataTransformationArtifact


class ModelPusher():

    def __init__(self, 
               model_pusher_config: ModelPusherConfig,
               data_transformation_artifact: artifact_entity.DataTransformationArtifact,
               model_trainer_artifact: artifact_entity.ModelTrainerArtifact):
        try:
            self.model_pusher_config = model_pusher_config
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_artifact= model_trainer_artifact
            self.model_resolver = ModelResolver(model_registry=self.model_pusher_config.saved_model_dir)
        except Exception as e:
            raise LeadException(e,sys)

    def initiate_model_pusher(self,)->ModelPusherArtifact:
        try:

            logging.info(f"Loading all objects")
            transformer = load_object(file_path= self.data_transformation_artifact.transform_object_path)
            model = load_object(file_path= self.model_trainer_artifact.model_path)
            target_encoder = load_object(file_path=self.data_transformation_artifact.target_encoder_path)

            logging.info(f"Saving object in Pusher Directory")
            save_object(file_path=self.model_pusher_config.pusher_transformer_path,obj = transformer)
            save_object(file_path=self.model_pusher_config.pusher_model_path, obj = model)
            save_object(file_path=self.model_pusher_config.pusher_target_encoder_path, obj=target_encoder)

            logging.info("Saving Model in Saved Model Directory")
            transformer_path = self.model_resolver.get_latest_save_transformer_path()
            model_path = self.model_resolver.get_latest_save_model_path()
            target_encoder_path = self.model_resolver.get_latest_save_target_encoder_path()

            save_object(file_path=transformer_path, obj = transformer)
            save_object(file_path=model_path, obj=model)
            save_object(file_path=target_encoder_path, obj=target_encoder)


            model_pusher_artifact = artifact_entity.ModelPusherArtifact(
                pusher_model_dir = self.model_pusher_config.pusher_model_dir,
                saved_model_dir = self.model_pusher_config.saved_model_dir)
            logging.info(f" Model Pusher Artifact : {model_pusher_artifact}")
            return model_pusher_artifact
        except Exception as e:
            raise LeadException(e, sys)