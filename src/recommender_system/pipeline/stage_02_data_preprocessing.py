from recommender_system.components import DataPreprocessor
from recommender_system.config import ConfigurationManager
from recommender_system.logging import logger


class DataPreprocessingPipeline:
    def __init__(self):
        pass

    def main(self):
        """Executes the main data preprocessing pipeline steps."""
        config = ConfigurationManager()
        data_preprocessing_config = config.get_data_preprocessing_config()
        data_preprocessor = DataPreprocessor(data_preprocessing_config)
        data_preprocessor.load_data()
        data_preprocessor.encode_labels()
        data_preprocessor.calculate_statistics()
        data_preprocessor.prepare_data()
        data_preprocessor.save_preprocessed_data()
