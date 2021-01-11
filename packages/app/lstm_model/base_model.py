from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.callbacks import EarlyStopping
from keras.layers import Dense,  Activation, LSTM, ReLU, Embedding
from keras.optimizers import Adam
from loguru import logger
import pandas as pd
import pickle
import toml
import os
import re


from lstm_model.utils import rmsle, make_pass_token, list_merge


class PasswordLSTM:
    """ LSTM model to predict password frequency"""

    def __init__(self, model_serialized=None, tokenizer=None):
        """
        Initialize model configuration
        @param model_serialized: model file
        @param tokenizer: tokenizer file
        """
        self.config = toml.load('config.toml')
        self.data_dir = self.config['project']['data_dir']
        self.res_dir = self.config['project']['resources_path']

        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        self.model = None
        if model_serialized:
            self.model = load_model(
                os.path.join(self.res_dir, model_serialized),
                custom_objects={'rmsle': rmsle}, compile=False
            )
        self.tokenizer = None
        if tokenizer:
            self.tokenizer = os.path.join(self.res_dir, tokenizer)

    def predict(self, password: str) -> float:
        """Predict password frequency
        @param password: unique password
        @return: predicted frequency
        """
        token = make_pass_token(self.tokenizer, password)
        y_pred = self.model.predict(token, batch_size=1)
        return y_pred[0][0]

    def _load_data(self, train_file: str, test_file: str) -> object:
        """
        Load and basic processing of train and test data
        @param train_file: zip file for train data
        @param test_file: zip file for test data
        @return: y: pass frequency, full_df: train+test passes, n_train_recs: count of train records
        """
        train_data = pd.read_csv(os.path.join(self.data_dir, train_file), compression='zip')
        test_data = pd.read_csv(os.path.join(self.data_dir, test_file), compression='zip')
        train_data.dropna(inplace=True)
        y = train_data.Times
        train_data.drop(columns='Times', inplace=True)
        test_data.drop(columns='Id', inplace=True)
        full_df = train_data.append(test_data)
        n_train_recs = train_data.shape[0]
        logger.info('data loading .. done')
        return y, full_df, n_train_recs

    @staticmethod
    def _process_pass_data(data):
        """
        Preprocessing for common data
        @param data:
        @return: data: dataframe with processed passes, max_pass_len: max length for pass in train and test,
         dict_len: count of symbols
        """
        data['len'] = data['Password'].apply(lambda x: len(str(x)))
        data['Password'] = data['Password'].apply(lambda x: ' '.join(re.findall('\S', str(x))))
        chars = data['Password'].apply(lambda x: str(x).split(' ')).values
        chars_dict = set(list_merge(chars))
        dict_len = len(chars_dict)
        max_pass_len = data['len'].max()
        logger.info('data processing .. done')
        return data, max_pass_len, dict_len

    def _fit_tokenizer(self, data: pd.DataFrame, dict_len: int, max_pass_len: int):
        """
        Create tokenizer for data and return dict_len and max_pass_len
        @rtype: object
        """
        self.tokenizer = Tokenizer(dict_len, filters='', lower=False)
        self.tokenizer.fit_on_texts(data['Password'])
        data_tokens = self.tokenizer.texts_to_sequences(data['Password'])
        logger.info('fit tokenizer .. done')
        return pad_sequences(data_tokens, max_pass_len, padding='post')

    def save_tokenizer(self, tokenizer_name: str):
        """
        Save tokenizer
        @param tokenizer_name:
        @return: None
        """
        full_name = os.path.join(self.res_dir, tokenizer_name)
        with open(full_name, 'wb') as handle:
            pickle.dump(self.tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
        logger.info('save tokenizer .. done')
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
            x, y_data,
            test_size=test_size,
            train_size=1-test_size,
            random_state=random_state
        )
        logger.info('split data .. done')
        return x_train, x_val, y_train, y_val, x_test

    def fit(self, train_file: str, test_file: str, epochs: int, batch_size: int, test_size=0.1, random_state=42):
        """
        Train model
        @param train_file:
        @param test_file:
        @param epochs:
        @param batch_size:
        @param test_size:
        @param random_state:
        """
        y, full_df, n_train_recs = self._load_data(train_file, test_file)
        full_df, max_pass_len, dict_len = self._process_pass_data(full_df)
        data_tokenized = self._fit_tokenizer(full_df, dict_len, max_pass_len)
        x_train, x_val, y_train, y_val, _ = self._split_data(
            data_tokenized, y, test_size=test_size, n_train_recs=n_train_recs, random_state=random_state
        )
        early_stopping = EarlyStopping(monitor='val_loss', patience=2, verbose=0, mode='auto')
        model = Sequential()
        model.add(
            Embedding(
                dict_len,
                self.config['model']['embedding_dim'],
                input_length=max_pass_len,
                mask_zero=True
            )
        )
        model.add(LSTM(self.config['model']['hidden_dim']))
        model.add(Dense(1))
        model.add(ReLU())
        model.compile(loss=rmsle, optimizer=Adam())
        logger.info('train model .. start')
        hist = model.fit(
            x_train, y_train,
            epochs=epochs, batch_size=batch_size,
            validation_data=(x_val, y_val),
            callbacks=[early_stopping]
        )
        self.model = model
        logger.info('train model .. done')
        return None

    def save_model(self, model_name: str):
        """
        Save lstm-model with model_name
        @param model_name:
        @return:
        """
        self.model.save(os.path.join(self.res_dir, model_name))
        logger.info('save model .. done')
        return None
