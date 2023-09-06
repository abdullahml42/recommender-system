import tensorflow as tf
from keras.layers import (Concatenate, Dense, Dropout, Embedding, Flatten,
                          Input, Multiply)
from keras.models import Model

from recommender_system.logging import logger


class ModelBuilder:
    def __init__(self, config):
        """Initialises the ModelBuilder object with the given config."""
        self.config = config

    def build_and_compile_model(self):
        """Builds and compiles the model."""
        number_of_reviewers = self.config.number_of_reviewers
        number_of_products = self.config.number_of_products
        number_of_dimensions = self.config.number_of_dimensions
        learning_rate = self.config.learning_rate

        reviewer_input = Input(shape=(1,))
        reviewer_embedding = Embedding(
            input_dim=number_of_reviewers, output_dim=number_of_dimensions
        )(reviewer_input)
        reviewer_embedding = Flatten()(reviewer_embedding)

        product_input = Input(shape=(1,))
        product_embedding = Embedding(
            input_dim=number_of_products, output_dim=number_of_dimensions
        )(product_input)
        product_embedding = Flatten()(product_embedding)

        matrix_factorisation_output = Multiply()(
            [reviewer_embedding, product_embedding]
        )
        concatenated_embeddings = Concatenate()([reviewer_embedding, product_embedding])

        hidden_layer_1 = Dense(units=32, activation="relu")(concatenated_embeddings)
        dropout_layer = Dropout(rate=0.5)(hidden_layer_1)
        hidden_layer_2 = Dense(units=16, activation="relu")(dropout_layer)

        output = Concatenate()([matrix_factorisation_output, hidden_layer_2])
        output = Dense(units=1, activation="sigmoid")(output)

        model = Model(inputs=[reviewer_input, product_input], outputs=output)
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
            loss="mse",
            metrics=["accuracy"]
        )

        return model

    def save_model(self, model):
        """Saves the model."""
        model.save(self.config.model_path)
