import sys
import os
import ast
import json
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import numpy as np



def main():
    tweet_data = pd.read_csv("SentimentDates.csv")
    stock_data = pd.read_csv("aaplStock.csv")
    
    tweet_data.sort_values("Date", inplace=True)
    stock_data.sort_values("Date", inplace=True)
    
    # merge datasets
    whole_data = pd.merge(tweet_data, stock_data, on='Date')
    print(whole_data.head())

    # create feature series from merged dataframe
    closingPrice = whole_data['Close']
    closingPrice.index = whole_data['Date']
    sentimentsSum = whole_data['SentimentSum']
    sentimentsSum.index = whole_data['Date']
    
    print("Saving Whole data")
    whole_data.to_csv("merged_data.csv",index=False)

    # calculate daily changes
    N = closingPrice.shape[0]
    stockDailyChange = pd.Series(closingPrice[1:N].values - closingPrice[:N-1].values, index=closingPrice.index[1:])
    N = sentimentsSum.shape[0]
    sentimentDailyChange = pd.Series(sentimentsSum[1:N].values - sentimentsSum[:N-1].values, index=sentimentsSum.index[1:])
)
     
    # normalize daily changes for regression
    stockDailyChangeZ = ((stockDailyChange-stockDailyChange.mean())/stockDailyChange.std())
    sentimentDailyChangeZ = ((sentimentDailyChange-sentimentDailyChange.mean())/sentimentDailyChange.std())
    
    plt.figure()    
    # stockDailyChange.plot(kind='line', label='Daily Stock Change')
    stockDailyChangeZ.plot(kind='line', label='Normalized Daily Stock Change')
    sentimentDailyChangeZ.plot(kind='line', label='Normalized Daily Sentiment Change')


    plt.legend()
    plt.show()

    features = ['SentimentSum']
    y=sentimentDailyChangeZ
    X=stockDailyChange

    X = X.reshape((X.shape[0],1))
    #y = y.reshape((y.shape[0],1))
    print(X.shape)
    print(y.shape)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

    # Create linear regression object
    regr = linear_model.LinearRegression()

    # Fit regression model to the training set
    regr.fit(X_train, y_train)

    # Apply model to the test set
    y_pred_test = regr.predict(X_test)

    print("Root mean squared error = %.4f" % np.sqrt(mean_squared_error(y_test, y_pred_test)))
    print("R-square = %.4f" % r2_score(y_test, y_pred_test))
    print('Slope Coefficients:', regr.coef_)
    print('Intercept:', regr.intercept_)
    
    # Plot outputs
    plt.figure()
    plt.scatter(X_test, y_test,  color='black')
    plt.plot(X_test, y_pred_test, color='blue', linewidth=3)
    titlestr = 'Predicted Function: y = %.2fX + %.2f' % (regr.coef_[0], regr.intercept_)
    plt.title(titlestr)
    plt.xlabel('X')
    plt.ylabel('y')
    plt.legend()
    plt.show()
    
if __name__ == "__main__":
    main()