from recommender_system.components import ModelTrainer
from recommender_system.config import ConfigurationManager
from recommender_system.logging import logger


class ModelTrainerPipeline:
    def __init__(self):
        pass

    def main(self):
        """Executes the main model training pipeline steps."""
        config = ConfigurationManager()
        train_config = config.get_train_model_config()
        model_trainer = ModelTrainer(train_config)
        history = model_trainer.train_model()
