from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionConfig:
    """Represents the configuration for data ingestion."""
    root_dir: Path
    source_url: str
    local_data_file_path: Path
    unzip_directory: Path
