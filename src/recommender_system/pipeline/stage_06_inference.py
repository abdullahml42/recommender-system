import os
import pickle

import numpy as np
import pandas as pd
import yaml
from tensorflow.keras.models import load_model

from recommender_system.utils import unscale_targets


class RecommendProducts:
    def __init__(self, reviewer_id):
        self.reviewer_id = reviewer_id

    def load_model(self):
        """Loads the trained model."""
        model_path = os.path.join("artifacts", "train_model", "trained_model.h5")
        self.model = load_model(model_path)

    def load_data(self):
        """Loads the preprocessed data."""
        data_path = os.path.join(
            "artifacts", "data_preprocessing", "preprocessed_data.csv"
        )
        self.df = pd.read_csv(data_path)

    def load_reviewer_encoder(self):
        """Loads the reviewer encoder used for preprocessing reviewer IDs."""
        reviewer_encoder_path = os.path.join(
            "artifacts", "data_preprocessing", "reviewer_encoder.pkl"
        )
        with open(reviewer_encoder_path, "rb") as f:
            self.reviewer_encoder = pickle.load(f)

    def load_params(self):
        """Loads the parameters used for generating recommendations."""
        params_path = os.path.join("params", "params.yaml")
        with open(params_path, "r") as f:
            self.params = yaml.safe_load(f)
        self.min_rating = self.params["MIN_RATING"]
        self.max_rating = self.params["MAX_RATING"]

    def preprocess_reviewer(self):
        """Preprocesses the reviewer ID by encoding it using the reviewer encoder."""
        encoded_reviewer_id = self.reviewer_encoder.transform([self.reviewer_id])
        return encoded_reviewer_id

    def preprocess_rated_products(self):
        """Returns the products rated by the reviewer and their corresponding encoded IDs."""
        rated_products_id = list(
            self.df[self.df["reviewerID"] == self.reviewer_id]["productID"]
        )
        encoded_rated_products_id = list(
            self.df[self.df["reviewerID"] == self.reviewer_id]["encodedProductID"]
        )

        return rated_products_id, encoded_rated_products_id

    def find_unrated_products(self, encoded_rated_products_id):
        """Finds the unrated products for the given reviewer."""
        unrated_products = []
        for i in range(
            min(self.df["encodedProductID"]), max(self.df["encodedProductID"]) + 1
        ):
            if i not in encoded_rated_products_id:
                unrated_products.append(i)

        return unrated_products

    def make_predictions(self, encoded_reviewer_id, unrated_products):
        """Makes predictions for the unrated products using the trained model."""
        example = [
            np.asarray(list(encoded_reviewer_id) * len(unrated_products)),
            np.asarray(unrated_products)
        ]
        predicted_ratings = self.model.predict(example, verbose=0)
        predicted_ratings = unscale_targets(
            predicted_ratings, self.min_rating, self.max_rating
        )

        return predicted_ratings

    def generate_recommendations(self, unrated_products, predicted_ratings, num_items):
        """Generates recommendations based on the predicted ratings for the unrated products."""
        test_df = pd.DataFrame(unrated_products, columns=["encodedProductID"])
        test_df["predictedRating"] = predicted_ratings
        test_df = test_df.merge(
            self.df, on="encodedProductID", how="left"
        ).drop_duplicates(subset="productID")
        test_df = test_df[["productID", "predictedRating"]].sort_values(
            "predictedRating", ascending=False
        )
        test_df = test_df.rename(columns={"productID": "recommendedProductID"})
        recommendations = test_df.head(num_items)

        return recommendations

    def recommend_products(self, num_items):
        """Recommends a specified number of products for the reviewer."""
        self.load_model()
        self.load_data()
        self.load_reviewer_encoder()
        self.load_params()
        encoded_reviewer_id = self.preprocess_reviewer()
        rated_products_id, encoded_rated_products_id = self.preprocess_rated_products()
        unrated_products = self.find_unrated_products(encoded_rated_products_id)
        predicted_ratings = self.make_predictions(encoded_reviewer_id, unrated_products)
        recommendations = self.generate_recommendations(
            unrated_products, predicted_ratings, num_items
        )

        return recommendations
