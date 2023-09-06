from recommender_system.components import ModelBuilder
from recommender_system.config import ConfigurationManager
from recommender_system.logging import logger


class ModelBuilderPipeline:
    def __init__(self):
        pass

    def main(self):
        """Executes the main model building pipeline steps."""
        config = ConfigurationManager()
        model_config = config.get_build_model_config()
        model_builder = ModelBuilder(model_config)
        model = model_builder.build_and_compile_model()
        model_builder.save_model(model)
