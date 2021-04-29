import os
import json
from sys import argv
import toml

import numpy as np
import pandas as pd

from lstm_model.base_model import PasswordLSTM


def rmlse(y_true, y_pred):
    y_true_log = np.log10(1 + y_true)
    y_pred_log =  np.log10(1 + y_pred)
    value = np.mean((y_true_log - y_pred_log) ** 2) ** 0.5
    return value


def calc_metrics(y_true, y_pred):
    values = {
        'rmlse': rmlse(y_true, y_pred)
    }
    return values


def main():
    config = toml.load("config.toml")
    target = config['columns']['target']
    Id = config['columns']['Id']
    data_folder, model_folder = argv[1], argv[2]
    train = pd.read_csv(os.path.join(data_folder, "train.csv"))
    val = pd.read_csv(os.path.join(data_folder, "val.csv"))
    test = pd.read_csv(os.path.join(data_folder, "test.csv"))
    # TODO: need to read model folder and pass it to PasswordModel
    password_model = PasswordLSTM(config=config)
    # TODO: read params from config
    params = dict(epochs=1, batch_size=512)
    password_model.fit(
        train_data=train, test_data=val.drop(columns=[target]), **params
    )
    # save artifacts
    tokenizer_path = os.path.join(model_folder, "tokenizer.pickle")
    model_path = os.path.join(model_folder, "one_epoch_model")
    os.mkdir('model')
    password_model.save_tokenizer(tokenizer_path)
    password_model.save_model(model_path)

    # validate metric quality - and load the model to check it fully
    password_model_loaded = PasswordLSTM(config=config, model_serialized=model_path, tokenizer=tokenizer_path)
    val_prediction = password_model_loaded.predict(val.drop(columns=[target]))
    
    # calc metrics
    metrics = calc_metrics(val[target].values, val_prediction)
    with open('metrics.json', 'w+') as f:
        json.dump(metrics, f)
    
    # retrain model on full data
    password_model.fit(
        train_data=pd.concat([train, val]), test_data=test.drop(columns=[Id]), **params
    )
    password_model.save_tokenizer("tokenizer.pickle")
    password_model.save_model("one_epoch_model")


if __name__ == "__main__":
    main()
