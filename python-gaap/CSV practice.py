import pandas as pd

notify_usage = pd.read_csv("./Notify Usage.csv")

print(notify_usage.sample(100))

print(notify_usage.dtypes)