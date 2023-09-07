import pickle
from pathlib import Path

import numpy as np
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

seed_value = 42
np.random.seed(seed_value)
tf.random.set_seed(seed_value)


class ModelTrainer:
    def __init__(self, config):
        """Initialises the ModelTrainer object with the given config."""
        self.config = config

    def get_base_model(self):
        """Returns the base model."""
        return tf.keras.models.load_model(self.config.base_model_path)

    def load_data(self, data_file_path):
        """Loads and returns data."""
        with data_file_path.open("rb") as f:
            data = pickle.load(f)

        return data

    def get_data(self):
        """Returns the loaded training and validation data."""
        data_dir = self.config.data_path

        X_train = self.load_data(data_dir / "X_train.pkl")
        X_val = self.load_data(data_dir / "X_val.pkl")
        y_train_scaled = self.load_data(data_dir / "y_train_scaled.pkl")
        y_val_scaled = self.load_data(data_dir / "y_val_scaled.pkl")

        return X_train, X_val, y_train_scaled, y_val_scaled

    def get_checkpoint_best_only(self):
        """Returns the checkpoint callback for saving the best model."""
        checkpoint_path = str(self.config.trained_model_path)

        checkpoints = ModelCheckpoint(
            filepath=checkpoint_path,
            monitor="val_accuracy",
            verbose=self.config.verbose,
            save_best_only=True,
            save_weights_only=False,
            save_freq="epoch"
        )

        return checkpoints

    def get_early_stopping(self):
        """Returns the early stopping callback."""
        callback = EarlyStopping(
            patience=2, monitor="val_loss", verbose=self.config.verbose
        )

        return callback

    def initialise_callbacks(self):
        """Initialises and returns the list of callbacks."""
        checkpoint_best_only = self.get_checkpoint_best_only()
        early_stopping = self.get_early_stopping()
        callbacks = [checkpoint_best_only, early_stopping]

        return callbacks

    def train_model(self):
        """Trains the model and returns the training history."""
        X_train, X_val, y_train_scaled, y_val_scaled = self.get_data()
        model = self.get_base_model()
        callbacks = self.initialise_callbacks()

        history = model.fit(
            X_train,
            y_train_scaled,
            batch_size=self.config.batch_size,
            epochs=self.config.epochs,
            verbose=self.config.verbose,
            callbacks=callbacks,
            validation_data=(X_val, y_val_scaled)
        )

        return history
