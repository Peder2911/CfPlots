import logging
from __app__.plot import outputPlot
from __app__.settings import SETTINGS

import pandas as pd
import numpy as np

from matplotlib import pyplot as plt
import matplotlib

from datetime import datetime

import requests

import json

import re

@outputPlot
def main(*args,**kwargs):
    plt.clf()

    try:
        country = kwargs["country"]
        filterString = f'(country:"{country}")'
    except KeyError:
        filterString = "" 

    query = """
        query{
            ceasefires~FILTERSTRING~{
                effectDate
        }}"""
    query = re.sub("~FILTERSTRING~",filterString,query)

    d = requests.post(SETTINGS["api"],data={"query":query})
    if d.status_code != 200:
        raise Exception(f"API had {d.status_code} status code: {d.text}")

    try:
        data = pd.DataFrame(d.json()["data"]["ceasefires"])
    except Exception as e:
        raise e

    data = data[data["effectDate"].apply(lambda x: x is not None)]

    data["effectDate"] = data["effectDate"].apply(lambda x: datetime.strptime(x,"%Y-%m-%d"))

    dates = matplotlib.dates.date2num(data["effectDate"])
    dates.sort()

    values = np.full(len(dates),1)
    fig,ax = plt.subplots()
    plt.stem(dates,values)
