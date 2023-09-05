import os
from pathlib import Path

from recommender_system.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH
from recommender_system.entity import (DataIngestionConfig,
                                       DataPreprocessingConfig)
from recommender_system.utils import create_directories, read_yaml


class ConfigurationManager:
    def __init__(
        self, config_filepath=CONFIG_FILE_PATH, params_filepath=PARAMS_FILE_PATH
    ):
        """Initialises ConfigurationManager with config and params filepaths."""
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        """Returns the data ingestion configuration."""
        config = self.config.data_ingestion
        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=Path(config.root_dir),
            source_url=config.source_url,
            local_data_file_path=Path(config.local_data_file_path),
            unzip_directory=Path(config.unzip_directory),
        )

        return data_ingestion_config

    def get_data_preprocessing_config(self) -> DataPreprocessingConfig:
        """Returns the data preprocessing configuration."""
        config = self.config.data_preprocessing
        create_directories([config.root_dir])

        data_preprocessing_config = DataPreprocessingConfig(
            root_dir=Path(config.root_dir), data_path=Path(config.data_path)
        )

        return data_preprocessing_config
