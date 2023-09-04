from recommender_system.components import DataIngestion
from recommender_system.config import ConfigurationManager
from recommender_system.logging import logger


class DataIngestionPipeline:
    def __init__(self):
        pass

    def main(self):
        """Executes the main data ingestion pipeline steps."""
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        data_ingestion = DataIngestion(data_ingestion_config)
        data_ingestion.download_data()
        data_ingestion.extract_and_rename_json()
