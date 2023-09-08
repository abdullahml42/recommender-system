from recommender_system.components import EvaluateModel
from recommender_system.config import ConfigurationManager
from recommender_system.logging import logger


class ModelEvaluationPipeline:
    def __init__(self):
        pass

    def main(self):
        """Executes the main model evaluation pipeline steps."""
        config_manager = ConfigurationManager()
        evaluation_config = config_manager.get_evaluate_model_config()
        evaluate_model = EvaluateModel(evaluation_config)
        evaluate_model.generate_predictions()
        evaluation_results = evaluate_model.evaluate()
        ranking_results = evaluate_model.ranking_evaluation()
