import os
import sys
import pandas as pd
import numpy as np
from leads.logger import logging
from leads.exception import LeadException
from leads.entity import config_entity, artifact_entity
from leads import utils
from leads.components import data_ingestion, data_transformation, data_validation
from leads.config import TARGET_COLUMN

class ModelEvaluation():

    def __init__(self,
                model_eval_config:config_entity.ModelEvaluationonfig,
                data_ingestion_artifact:artifact_entity.DataIngestionArtifact,
                data_transformation_artifact:artifact_entity.DataTransformationArtifact,
                model_trainer_artifact:artifact_entity.ModelTrainerArtifact,
               ):
      try:
        logging.info(f"{'>>'*20} Model Evaluation {'<<'*20}")
        self.model_eval_config = model_eval_config,
        self.data_ingestion_artifact = data_ingestion_artifact,
        self.data_transformation_artifact = data_transformation_artifact,
        self.model_trainer_artifact = model_trainer_artifact,
        self.model_resolver = ModelResolver()
      except Exception as e:
        raise LeadException(e, sys)

    def initiate_model_evaluation(self)-> artifact_entity.ModelEvaluationArtifact:
        