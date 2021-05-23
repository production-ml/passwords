import os
from sys import argv

import pandas as pd


def split_data(df: pd.DataFrame):
    """
    Split data to train and test
    """
    # dumb option for a start
    train = df.iloc[::2]
    val = df.iloc[1::2]
    return train, val


def process(train_data: pd.DataFrame, test_data: pd.DataFrame) -> object:
    """
    Basic processing of train and test data
    @param train_file: DataFrame for train data
    @param test_file: DataFrame for test data
        test data could be some "golden set" in a real world scenario, used to validate model quality
    @return: train and test dataframes
    """
    # mimic the situation where data changes every day
    # note, that more realistic way would be to do this on the initial data before aggregation
    seed = pd.Timestamp.now().date().toordinal()
    train_data = train_data.sample(frac=0.5, random_state=seed)

    # some data processing
    train_data.dropna(inplace=True)
    train, val = split_data(train_data)

    return train, val, test_data


if __name__ == "__main__":
    train_file, test_file, output_folder = argv[1], argv[2], argv[3]
    train_data = pd.read_csv(train_file, compression="zip")
    test_data = pd.read_csv(test_file, compression="zip")

    train, val, test = process(train_data, test_data)
    os.mkdir(output_folder)
    train.to_csv(os.path.join(output_folder, "train.csv"), index=False)
    val.to_csv(os.path.join(output_folder, "val.csv"), index=False)
    test.to_csv(os.path.join(output_folder, "test.csv"), index=False)
