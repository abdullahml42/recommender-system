from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionConfig:
    """Represents the configuration for data ingestion."""
    root_dir: Path
    source_url: str
    local_data_file_path: Path
    unzip_directory: Path


@dataclass(frozen=True)
class DataPreprocessingConfig:
    """Represents the configuration for data preprocessing."""
    root_dir: Path
    data_path: Path


@dataclass(frozen=True)
class ModelConfig:
    """Represents the configuration for building the model."""
    root_dir: Path
    model_path: Path
    number_of_reviewers: int
    number_of_products: int
    number_of_dimensions: int
    learning_rate: float


@dataclass(frozen=True)
class TrainModelConfig:
    """Represents the configuration for training the model."""
    root_dir: Path
    base_model_path: Path
    trained_model_path: Path
    data_path: Path
    batch_size: int
    epochs: int
    verbose: int
    