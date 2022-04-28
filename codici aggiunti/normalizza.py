import pandas 
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import matplotlib.pyplot as plt

import numpy as np
df=pandas.read_csv("C:/Users/Utente/Desktop/dataset1/interessi_dataset.csv")

def minmax_norm(df_input):
    return (df - df.min()) / ( df.max() - df.min())

df["sport2"] = pd.cut(df["sport"],
 bins=[0., 1.5, 3.0, 4.5, 6., np.inf],
 labels=[1, 2, 3, 4, 5])

print(minmax_norm(df))

