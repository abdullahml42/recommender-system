import os
import pickle
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from recommender_system.logging import logger
from recommender_system.utils import scale_targets


class DataPreprocessor:
    def __init__(self, config):
        """Initialises the DataPreprocessor object with the given config."""
        self.config = config

    def load_data(self):
        """Loads data from a JSON file and performs initial data preprocessing."""
        self.df = pd.read_json(self.config.data_path, lines=True)
        self.df = self.df[["reviewerID", "asin", "overall"]]
        self.df = self.df.rename(columns={"asin": "productID", "overall": "rating"})
        self.df = self.df.groupby(by=["reviewerID", "productID"], as_index=False).agg(
            {"rating": "mean"}
        )

    def encode_labels(self):
        """Encodes reviewer and product labels using LabelEncoder."""
        self.reviewer_encoder = LabelEncoder()
        self.df["encodedReviewerID"] = self.reviewer_encoder.fit_transform(
            self.df["reviewerID"]
        )

        self.product_encoder = LabelEncoder()
        self.df["encodedProductID"] = self.product_encoder.fit_transform(
            self.df["productID"]
        )

    def calculate_statistics(self):
        """Calculates statistics."""
        self.number_of_reviewers = self.df["encodedReviewerID"].nunique()
        self.number_of_products = self.df["encodedProductID"].nunique()
        self.min_rating = np.min(self.df["rating"])
        self.max_rating = np.max(self.df["rating"])
        self.save_params()

    def prepare_data(self):
        """Prepares the features and targets for training and validation."""
        features = self.df[["encodedReviewerID", "encodedProductID"]]
        targets = self.df["rating"]

        self.X_train, self.X_val, self.y_train, self.y_val = train_test_split(
            features.values, targets.values, test_size=0.2, random_state=1
        )

        self.X_train_lists = [self.X_train[:, 0], self.X_train[:, 1]]
        self.X_val_lists = [self.X_val[:, 0], self.X_val[:, 1]]
        self.val_reviewer_ids = self.X_val[:, 0]
        self.val_product_ids = self.X_val[:, 1]

        self.y_train_scaled = scale_targets(
            self.y_train, self.min_rating, self.max_rating
        )
        self.y_val_scaled = scale_targets(self.y_val, self.min_rating, self.max_rating)

    def save_params(self):
        """Saves the parameters."""
        params_file_path = Path("params/params.yaml")

        if params_file_path.exists():
            with open(params_file_path, "r") as f:
                params = yaml.safe_load(f)
        else:
            params = {}

        params["NUMBER_OF_REVIEWERS"] = int(self.number_of_reviewers)
        params["NUMBER_OF_PRODUCTS"] = int(self.number_of_products)
        params["MIN_RATING"] = float(self.min_rating)
        params["MAX_RATING"] = float(self.max_rating)

        with open(params_file_path, "w") as f:
            yaml.dump(params, f)

    def save_preprocessed_data(self):
        """Saves preprocessed variables and objects."""
        os.makedirs(self.config.root_dir, exist_ok=True)

        self.df.to_csv(
            os.path.join(self.config.root_dir, "preprocessed_data.csv"), index=False
        )

        file_data = {
            "reviewer_encoder.pkl": self.reviewer_encoder,
            "product_encoder.pkl": self.product_encoder,
            "X_train.pkl": self.X_train_lists,
            "X_val.pkl": self.X_val_lists,
            "y_train_scaled.pkl": self.y_train_scaled,
            "y_val_scaled.pkl": self.y_val_scaled,
            "val_reviewer_ids.pkl": self.val_reviewer_ids,
            "val_product_ids.pkl": self.val_product_ids
        }

        for filename, data in file_data.items():
            with open(os.path.join(self.config.root_dir, filename), "wb") as f:
                pickle.dump(data, f)
