import json
import pickle
from pathlib import Path

import numpy as np
import tensorflow as tf
from sklearn.metrics import (mean_absolute_error,
                             mean_absolute_percentage_error,
                             mean_squared_error, r2_score)

from recommender_system.utils import unscale_targets


class EvaluateModel:
    def __init__(self, config):
        """Initialises the EvaluateModel object with the given config."""
        self.config = config

    def load_trained_model(self):
        """Loads the trained model."""
        return tf.keras.models.load_model(self.config.trained_model_path)

    def load_data(self):
        """Loads and returns the required data for evaluation."""
        data_path = Path(self.config.data_path)
        pickle_files = [
            "X_val.pkl",
            "y_val_scaled.pkl",
            "val_reviewer_ids.pkl",
            "val_product_ids.pkl"
        ]

        loaded_data = {}
        for file_name in pickle_files:
            file_path = data_path / file_name
            with open(file_path, "rb") as f:
                loaded_data[file_name] = pickle.load(f)

        X_val = loaded_data["X_val.pkl"]
        y_val_scaled = loaded_data["y_val_scaled.pkl"]
        self.y_val_original = unscale_targets(
            y_val_scaled, self.config.min_rating, self.config.max_rating
        )
        self.val_reviewer_ids = loaded_data["val_reviewer_ids.pkl"]
        self.val_product_ids = loaded_data["val_product_ids.pkl"]

        return (
            X_val,
            y_val_scaled,
            self.y_val_original,
            self.val_reviewer_ids,
            self.val_product_ids
        )

    def generate_predictions(self):
        """Generates predictions using the trained model."""
        model = self.load_trained_model()
        X_val, _, _, _, _ = self.load_data()
        self.y_hat = model.predict(X_val, verbose=self.config.verbose)

    def evaluate(self):
        """Calculates evaluation metrics between ground truth y and predicted y_hat."""
        _, self.y, _, _, _ = self.load_data()
        evaluation_results = {
            "R2": r2_score(self.y, self.y_hat),
            "MAE": mean_absolute_error(self.y, self.y_hat),
            "MAPE": mean_absolute_percentage_error(self.y, self.y_hat),
            "MSE": mean_squared_error(self.y, self.y_hat),
            "RMSE": np.sqrt(mean_squared_error(self.y, self.y_hat))
        }

        results_filepath = Path(self.config.root_dir) / "evaluation_results.json"
        with open(results_filepath, "w") as f:
            json.dump(evaluation_results, f)

        return evaluation_results

    def calculate_dcg(self, relevance_scores, k):
        """Calculates Discounted Cumulative Gain (DCG) at position k."""
        relevance_scores = relevance_scores[:k]
        positions = np.arange(2, len(relevance_scores) + 2)
        dcg = np.sum(relevance_scores / np.log2(positions))
        return dcg

    def calculate_ndcg(self, relevance_scores, k):
        """Calculates Normalised Discounted Cumulative Gain (NDCG) at position k."""
        sorted_scores = sorted(relevance_scores, reverse=True)
        dcg_max = self.calculate_dcg(sorted_scores, k)
        dcg = self.calculate_dcg(relevance_scores, k)
        ndcg = dcg / dcg_max if dcg_max != 0 else 0
        return ndcg

    def ranking_evaluation(self, k=10):
        """Performs ranking evaluation using NDCG."""
        ndcgs = []

        for reviewer in np.unique(self.val_reviewer_ids):
            target_val_product_ids = self.val_product_ids[
                self.val_reviewer_ids == reviewer
            ]
            target_val_ratings = self.y_val_original[self.val_reviewer_ids == reviewer]
            ndcg = self.calculate_ndcg(
                target_val_ratings[
                    np.argsort(-self.y_hat[self.val_reviewer_ids == reviewer])
                ],
                k=k
            )
            ndcgs.append(ndcg)

        ndcg = np.mean(ndcgs)

        results_filepath = Path(self.config.root_dir) / "ndcg_result.json"
        with open(results_filepath, "w") as f:
            json.dump({"NDCG": ndcg}, f)

        return ndcg
        