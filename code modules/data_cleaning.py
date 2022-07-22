import re

import numpy as np
import pandas as pd


def data_cleaning(data):
    # remove_invalid_row(data)
    filter_size(data)
    filter_installs(data)
    filter_price(data)


# def remove_invalid_row(data):
#     for index, category in enumerate(data['Category']):
#         try:
#             float(category)
#             data.drop(index, axis=0, inplace=True)
#         except ValueError:
#             pass


def filter_size(data):
    for index, size in enumerate(data['Size']):
        if size[-1] == "k":
            data.at[index, 'Size'] = int(re.findall(r'\d+', size)[0]) / 1000

    data['Size'] = data.Size.replace("Varies with device", np.nan)
    data['Size'] = data.Size.str.replace("M", "")
    data['Size'] = pd.to_numeric(data['Size'], errors='coerce')


def filter_installs(data):
    data['Installs'] = data.Installs.str.replace(',', '', regex=False)
    data['Installs'] = data.Installs.str.replace('+', '', regex=False)
    data['Installs'] = data.Installs.replace("Free", np.nan)
    data['Installs'] = pd.to_numeric(data['Installs'], errors='coerce')


def filter_price(data):
    data['Price'] = data.Price.replace("Everyone", np.nan)
    data['Price'] = data.Price.str.replace("$", "", regex=False)
    data['Price'] = pd.to_numeric(data['Price'], errors='coerce')
