import pickle
import os
import re
from typing import Union

from sklearn.model_selection import train_test_split
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Dense, Activation, LSTM, ReLU, Embedding
from tensorflow.keras.optimizers import Adam
from loguru import logger
import pandas as pd
import numpy as np

# relative imports point to local modules instead of global
from .utils import rmsle, make_pass_token, list_merge


class PasswordLSTM:
    """ LSTM model to predict password frequency"""

    def __init__(self, config, model_serialized=None, tokenizer=None):
        """
        Initialize model configuration
        @param model_serialized: model file
        @param tokenizer: tokenizer file
        """
        self.config = config
        self.model = None
        self.tokenizer = None
        # read if provided
        if model_serialized:
            self.model = load_model(
                model_serialized,
                custom_objects={"rmsle": rmsle},
                compile=False,
            )
        if tokenizer:
            with open(tokenizer, "rb") as handle:
                self.tokenizer = pickle.load(handle)

    def predict_one(self, password: str) -> float:
        """Predict password frequency
        @param password: unique password
        @return: predicted frequency
        """
        token = make_pass_token(self.tokenizer, password)
        y_pred = self.model.predict(token, batch_size=1)
        return y_pred[0][0]

    def predict(self, password):
        # TODO: not very efficient, refactor
        if isinstance(password, str):
            return self.predict_one(password)
        else:
            return np.array([self.predict_one(p) for p in password])

    @staticmethod
    def _process_pass_data(data):
        """
        Preprocessing for common data
        @param data:
        @return: data: dataframe with processed passes, max_pass_len: max length for pass in train and test,
         dict_len: count of symbols
        """
        data["len"] = data["Password"].apply(lambda x: len(str(x)))
        data["Password"] = data["Password"].apply(
            lambda x: " ".join(re.findall("\S", str(x)))
        )
        chars = data["Password"].apply(lambda x: str(x).split(" ")).values

        chars_dict = set(list_merge(chars))
        dict_len = len(chars_dict)
        max_pass_len = data["len"].max()
        logger.info("data processing .. done")
        return data, max_pass_len, dict_len

    def _fit_tokenizer(self, data: pd.DataFrame, dict_len: int, max_pass_len: int):
        """
        Create tokenizer for data and return dict_len and max_pass_len
        @rtype: object
        """
        self.tokenizer = Tokenizer(dict_len, filters="", lower=False)
        self.tokenizer.fit_on_texts(data["Password"])
        data_tokens = self.tokenizer.texts_to_sequences(data["Password"])
        logger.info("fit tokenizer .. done")
        return pad_sequences(data_tokens, max_pass_len, padding="post")

    def save_tokenizer(self, tokenizer_name: str):
        """
        Save tokenizer
        @param tokenizer_name:
        @return: None
        """
        with open(tokenizer_name, "wb") as handle:
            pickle.dump(self.tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
        logger.info("save tokenizer .. done")
        return None

    @staticmethod
    def _split_data(x_data, y_data, test_size, n_train_recs, random_state):
        """
        Split data for train
        @param x_data:
        @param y_data:
        @param test_size:
        @param n_train_recs:
        @param random_state:
        @return:
        """
        x = x_data[:n_train_recs]  # train part
        x_test = x_data[n_train_recs:]  # test part
        x_train, x_val, y_train, y_val = train_test_split(
            x,
            y_data,
            test_size=test_size,
            train_size=1 - test_size,
            random_state=random_state,
        )
        logger.info("split data .. done")
        return x_train, x_val, y_train, y_val, x_test

    def get_model(self, dict_len, max_pass_len):
        model = Sequential()
        model.add(
            Embedding(
                dict_len,
                self.config["model"]["embedding_dim"],
                input_length=max_pass_len,
                mask_zero=True,
            )
        )
        model.add(LSTM(self.config["model"]["hidden_dim"]))
        model.add(Dense(1))
        model.add(ReLU())
        model.compile(loss=rmsle, optimizer=Adam())
        return model

    @staticmethod
    def process_data(train_data, test_data):
        y = train_data.Times
        train_data.drop(columns="Times", inplace=True)
        full_df = train_data.append(test_data)
        n_train_recs = train_data.shape[0]
        return y, full_df, n_train_recs

    def fit(
        self,
        train_data: pd.DataFrame,
        test_data: Union[pd.DataFrame, None],
        epochs: int,
        batch_size: int,
        test_size=0.1,
        random_state=42,
    ):
        """
        Train model
        @param train_data:
        @param test_data:
        @param epochs:
        @param batch_size:
        @param test_size:
        @param random_state:
        """
        # we use .copy() to avoid in-place modification of the dataset
        # these modifications could break something for the .fit() user
        y, full_df, n_train_recs = self.process_data(
            train_data.copy(), test_data.copy()
        )
        full_df, max_pass_len, dict_len = self._process_pass_data(full_df)
        data_tokenized = self._fit_tokenizer(full_df, dict_len, max_pass_len)
        x_train, x_val, y_train, y_val, _ = self._split_data(
            data_tokenized,
            y,
            test_size=test_size,
            n_train_recs=n_train_recs,
            random_state=random_state,
        )
        model = self.get_model(dict_len, max_pass_len)
        early_stopping = EarlyStopping(
            monitor="val_loss", patience=2, verbose=0, mode="auto"
        )
        logger.info("train model .. start")
        hist = model.fit(
            x_train,
            y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_data=(x_val, y_val),
            callbacks=[early_stopping],
        )
        self.model = model
        logger.info("train model .. done")
        return None

    def save_model(self, model_name: str):
        """
        Save lstm-model with model_name
        @param model_name:
        @return:
        """
        self.model.save(model_name)
        logger.info("save model .. done")
        return None
