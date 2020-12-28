import tensorflow as tf
import re
import pickle
from keras.preprocessing.sequence import pad_sequences

MAX_PASS_LEN = 42


def rmsle(y_true, y_pred):
    """Loss function"""
    return tf.sqrt(tf.reduce_mean(tf.squared_difference(tf.log1p(y_pred), tf.log1p(y_true))))


def make_pass_token(password: str):
    """Return sequence of tokens from password"""
    with open('models/tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
    password = ' '.join(re.findall('\S', str(password)))
    tokens = tokenizer.texts_to_sequences([password])
    tokens = pad_sequences(tokens, MAX_PASS_LEN, padding='post')
    return tokens
