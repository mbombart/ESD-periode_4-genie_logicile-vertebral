import argparse
import os
from random import shuffle

import pandas as pd
from sklearn.model_selection import train_test_split

from load_data import read_params


def split_data(df, train_data_path, test_data_path, split_ratio, random_state):
    """
    split data for data processing
    input: df : dataframe, path of data : str, ratio split : int, ramdon_state(seek): int
    output: df_train : dataframe, df_test : dataframe
    """
    # store feature matrix in "X"

    X = df.loc[:, ["0", "1", "2", "3", "4", "5"]]

    # store response vector in "y"
    y = df.loc[:, "6"]

    train, test = train_test_split(
        df, test_size=split_ratio, random_state=random_state, shuffle=True
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=split_ratio, random_state=random_state, shuffle=True
    )  # 70% training and 30% test

    df_train = X_train.merge(
        y_train, how="inner", left_index=True, right_index=True
    )
    df_train.to_csv(train_data_path, sep=",", index=False, encoding="utf-8")

    df_test = X_test.merge(
        y_test, how="inner", left_index=True, right_index=True
    )
    df_test.to_csv(test_data_path, sep=",", index=False, encoding="utf-8")

    return df_train, df_test


def split_and_saved_data(config_path):
    """
    split the train dataset(data/raw) and save it in the data/processed folder
    input: config path
    output: save splitted files in output folder
    """
    config = read_params(config_path)
    raw_data_path = config["raw_data_config"]["raw_data_csv"]
    test_data_path = config["processed_data_config"]["test_data_csv"]
    train_data_path = config["processed_data_config"]["train_data_csv"]
    split_ratio = config["raw_data_config"]["train_test_split_ratio"]
    random_state = config["raw_data_config"]["random_state"]
    raw_df = pd.read_csv(raw_data_path)
    split_data(
        raw_df, train_data_path, test_data_path, split_ratio, random_state
    )


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    split_and_saved_data(config_path=parsed_args.config)
    print("Succes")
