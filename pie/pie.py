import logging
from __app__.plot import outputPlot
from __app__.settings import SETTINGS

import pandas as pd
import numpy as np

from matplotlib import pyplot as plt
import matplotlib

from datetime import datetime

import requests

def pie(*args,**kwargs):
    plt.clf()
    d = requests.get(SETTINGS["api"]+"/ceasefires?country=100")
    if d.status_code != 200:
        raise Exception(f"API had {d.status_code} status code")

    try:
        data = pd.DataFrame(d.json())
    except Exception as e:
        raise e

    data["effect_date"] = data["effect_date"].apply(lambda x: datetime.strptime(x,"%Y-%m-%d"))

    dates = matplotlib.dates.date2num(data["effect_date"])
    dates.sort()

    values = np.full(len(dates),1)
    fig,ax = plt.subplots()
    plt.stem(dates,values)

main = outputPlot(pie)
