import os
import sys
from leads.entity import artifact_entity,config_entity
from leads.entity.artifact_entity import DataTransformationArtifact
from leads.config import TARGET_COLUMN
from leads.components import data_ingestion,data_transformation,data_validation
from leads.logger import logging
from leads.exception import LeadException
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from leads import utils
from leads.entity.artifact_entity import ModelTrainerArtifact

class ModelTrainer:

    def __init__(self,model_trainer_config:config_entity.ModelTrainerConfig,
                      data_transformation_artifact:artifact_entity.DataTransformationArtifact):
        try:
            logging.info(f"{'>>'*20} Model Trainer {'>>'*20}")
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise LeadException(e,sys)

    def train_model(self,x,y):
        try:
            xgb_clf = RandomForestClassifier()
            xgb_clf.fit(x,y)
            return xgb_clf
        except Exception as e:
            raise LeadException(e, sys)
    
    def initiate_model_trainer(self,)-> artifact_entity.ModelTrainerArtifact:
        try:
            logging.info(f"Loading Train Array and Test Array")
            train_arr = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_path)
            test_arr = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_path)

            logging.info(f"Splitting input feature into Train Array and Test Array")
            x_train,y_train = train_arr[:,:-1],train_arr[:,-1]
            x_test,y_test = test_arr[:,:-1],test_arr[:,-1]

            logging.info("Train Model")
            model = self.train_model(x=x_train,y=y_train)

            logging.info(f"Making Predictions and calculating F1_score for X_train")
            yhat_train = model.predict(x_train)
            f1_train_score = f1_score(y_true=y_train,y_pred=yhat_train)

            logging.info(f"Making Predications and calculating f1_score for X_tes")
            yhat_test = model.predict(x_test)
            f1_test_score = f1_score(y_true=y_test,y_pred=yhat_test)

            logging.info(f"train_score = {f1_train_score} and test_score = {f1_test_score}")

            logging.info(f"Checking if the model is underfitting or not ")
            if f1_test_score < self.model_trainer_config.expected_score:
                raise Exception(f" Model is not good as model is not expected to give \
                    expected accuracy : {self.model_trainer_config.expected_score} : \
                        model f1_score : {f1_test_score}")

            logging.info(f"Checking if the model is Overfitting or not")
            diff = abs(f1_train_score-f1_test_score)

            if diff > self.model_trainer_config.overfitting_threshold:
                raise Exception(f"Model is overfitted as diff between Train Score and Test Score : {f1_train_score} \
                                  is more than {self.model_trainer_config.overfitting_threshold}")
            
            logging.info(f"saving model object")
            utils.save_object(file_path=self.model_trainer_config.model_path, obj=model)

            logging.info(f"Preparing Model Artifact")
            
            model_trainer_artifact = artifact_entity.ModelTrainerArtifact(
                model_path= self.model_trainer_config.model_path ,
                f1_train_score= f1_train_score ,
                f1_test_score= f1_test_score)
            logging.info(f"Model Trainer Artifact : {model_trainer_artifact}")
            return model_trainer_artifact
            
        except Exception as e:
            raise LeadException(e, sys)


