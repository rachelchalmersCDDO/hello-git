
# pip install pandas, numpy and gender_guesser

import pandas as pd
import numpy as np
import gender_guesser.detector as gender

# import list of boys names as a test file

baby_names = pd.read_csv("./babies-first-names-19-full-list - babies-first-names-19-full-list.csv")

print("\n sample of raw data:\n")

print(baby_names.head(5))

# clean data: drop irrelevant columns and remove blank rows and columns

baby_names.drop(labels=["Unnamed: 3","Position.1","Name.1", "Number of babies.1"],axis=1, inplace=True)
baby_names.dropna(axis=1,how='all',inplace=True)
baby_names.dropna(axis=0,how='all',inplace=True)

print("\n sample of clean data:\n")

print(baby_names.head(5))
print("\n")

# create an array from the boys names column and print index 1 to return the list of names 

boys_names_column = baby_names.transpose().values.tolist()
print("\n")
print(boys_names_column[1])
print("\n")

# count types of gender by setting types dict to empty, for each name add the type returned to the dict

types = {}

d = gender.Detector()

for name in boys_names_column[1]:
	gender = d.get_gender(name)
	
	if gender not in types:
		types[gender] = 1
	else:
		types[gender] += 1

print(types)

