import os

import pandas as pd

ROOT_DIR = os.path.abspath(os.curdir)


def get_apps_data():
    return pd.read_csv(ROOT_DIR + "\\asserts\googleplaystore.csv")


def get_review_data():
    return pd.read_csv(ROOT_DIR + "\\asserts\googleplaystore_user_reviews.csv")
