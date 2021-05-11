import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

gapminder = pd.read_csv("./gapminder.csv")

# %matplotlib inline

figure, axes = plt.subplots()

figure, axes = plt.subplots(figsize=(8, 6)) # NEW - Set figure size

gm_1987 = gapminder[gapminder["year"] == 1987]
gm_1987.reset_index(drop = True, inplace = True)

figure, axes = plt.subplots(figsize=(6, 5))

axes.scatter(x=gm_1987["gdp_per_cap"], y=gm_1987["life_exp"])

while True:
	continue