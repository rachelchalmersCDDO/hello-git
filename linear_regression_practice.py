from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression 
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as seabornInstance 
from sklearn import metrics
from sklearn import datasets
from statsmodels.api import OLS
import statsmodels.api as sm
from statsmodels.sandbox.regression.predstd import wls_prediction_std

data,target = datasets.load_iris(return_X_y=True)

cancer_data = pd.read_csv("./cancer_reg.csv")
print(cancer_data.shape)
print(cancer_data.head())

cancer_data.plot(x='medIncome', y='avgDeathsPerYear', style='o')  
plt.title('medIncome vs avgDeathsPerYear')  
plt.xlabel('medIncome')  
plt.ylabel('avgDeathsPerYear')  
# plt.show()

plt.figure(figsize=(15,10))
plt.tight_layout()
seabornInstance.displot(cancer_data['medIncome'])
# plt.savefig('../displot.png')

X = cancer_data['medIncome'].values.reshape(-1,1)
y = cancer_data['avgDeathsPerYear'].values.reshape(-1,1)

# Next, we split 80% of the data to the training set while 20% of the data to test set using below code.
# The test_size variable is where we actually specify the proportion of the test set.

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# After splitting the data into training and testing sets, finally, the time is to train our algorithm. For that, we need to import LinearRegression class, instantiate it, and call the fit() method along with our training data.

regressor = LinearRegression()  
regressor.fit(X_train, y_train) #training the algorithm

#To retrieve the intercept:
print(regressor.intercept_)

#For retrieving the slope:
print(regressor.coef_)

print("this means for every unit change in median income, the change in average deaths is ", regressor.coef_)

y_pred = regressor.predict(X_test)

df = pd.DataFrame({'Actual': y_test.flatten(), 'Predicted': y_pred.flatten()})

df1 = df.head(25)
df1.plot(kind='bar',figsize=(16,10))
plt.grid(which='major', linestyle='-', linewidth='0.5', color='green')
plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
plt.savefig('../sampleplot.png')

print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))  
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))  
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))

cancer_data.loc['const'] = 1
reg1 = sm.OLS(endog=df1['avgDeathsPerYear'], exog=df1[['const', 'medIncome']], \
    missing='drop')
type(reg1)
results = reg1.fit()
type(results)
print(results.summary())

# res = sm.OLS(y, X).fit()
# print(res.summary())
















