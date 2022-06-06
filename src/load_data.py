import argparse
import io
import os
import zipfile
from random import shuffle

import pandas as pd
import requests
import yaml
from sklearn.model_selection import train_test_split

# from load_data import read_params


def read_params(config_path):
    """
    read parameters from the params.yaml file
    input: params.yaml location
    output: parameters as dictionary
    """
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


def load_data(config_path: str):
    """
    load data set from url
    input: model_var
    output:pandas dataframe
    """

    config = read_params(config_path)
    name_file = config["raw_data_config"]["name_file"]
    url = config["raw_data_config"]["chargement_data"]

    # load data
    r = requests.get(url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z = z.extract(name_file)
    df = pd.read_csv(name_file, header=None, sep=" ")
    os.remove(name_file)
    df.to_csv(config["raw_data_config"]["raw_data_csv"])

    return 0


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    load_data(config_path=parsed_args.config)
    print("Done")
