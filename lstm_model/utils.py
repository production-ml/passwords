import tensorflow as tf
import re
import pickle
from keras.preprocessing.sequence import pad_sequences
from flask import jsonify

MAX_PASS_LEN = 42


def rmsle(y_true, y_pred):
    """Loss function"""
    y_true = tf.cast(y_true, tf.float32)
    y_pred = tf.cast(y_pred, tf.float32)
    return tf.math.sqrt(
        tf.reduce_mean(
            tf.math.squared_difference(tf.math.log1p(y_pred), tf.math.log1p(y_true))
        )
    )


def make_pass_token(tokenizer, password: str):
    """Return sequence of tokens from password"""
    with open(tokenizer, "rb") as handle:
        tokenizer = pickle.load(handle)
    password = " ".join(re.findall("\S", str(password)))
    tokens = tokenizer.texts_to_sequences([password])
    tokens = pad_sequences(tokens, MAX_PASS_LEN, padding="post")
    return tokens


def list_merge(lstlst):
    all = []
    for lst in lstlst:
        all.extend(lst)
    return all


def response_json(password: str,  freq: float):
    """Response formatting as json"""
    res = jsonify(
        {
            "status": "success",
            "password": password,
            "prediction": f"{freq:.1f}"
        }
    )
    return res
