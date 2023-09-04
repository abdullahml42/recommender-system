import json
import os
from pathlib import Path
from typing import Union

import numpy as np
import yaml
from box import ConfigBox
from box.exceptions import BoxValueError
from ensure import ensure_annotations

from recommender_system.logging import logger


@ensure_annotations
def read_yaml(yaml_path: Path) -> ConfigBox:
    """Reads a YAML file and returns its content as a ConfigBox object."""
    try:
        with open(yaml_path) as file:
            yaml_content = yaml.safe_load(file)
            logger.info(f"Load YAML file: {yaml_path}")
            return ConfigBox(yaml_content)
    except BoxValueError:
        raise ValueError("YAML file is empty")
    except Exception as e:
        raise e


@ensure_annotations
def create_directories(directory_paths: list, verbose=True):
    """Creates directories based on the provided paths."""
    for path in directory_paths:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"Create directory at: {path}")


@ensure_annotations
def save_json(json_path: Path, data: dict):
    """Saves a JSON file at a specified file path."""
    with open(json_path, "w") as file:
        json.dump(data, file, indent=4)

    logger.info(f"Save JSON file at: {json_path}")


@ensure_annotations
def load_json(json_path: Path) -> ConfigBox:
    """Loads a JSON file and returns its content as a ConfigBox object."""
    with open(json_path) as file:
        json_content = json.load(file)

    logger.info(f"Load JSON file successfully from: {json_path}")
    return ConfigBox(json_content)


@ensure_annotations
def get_size(file_path: Path) -> str:
    """Returns the size of a file in kilobytes (KB) as a string."""
    size_in_kb = round(os.path.getsize(file_path) / 1024)
    return f"~ {size_in_kb} KB"


@ensure_annotations
def scale_targets(
    y: Union[float, np.ndarray], min_rating: float, max_rating: float
) -> np.ndarray:
    """Scales target values to a normalised range between 0 and 1."""
    return (y - min_rating) / (max_rating - min_rating)


@ensure_annotations
def unscale_targets(
    y: Union[float, np.ndarray], min_rating: float, max_rating: float
) -> np.ndarray:
    """Unscales target values from the normalised range back to the original range."""
    return (y * (max_rating - min_rating)) + min_rating
