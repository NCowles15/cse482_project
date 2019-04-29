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
    data = pd.read_csv("aaplStock.csv")
    # print(stock_data.shape)

    plt.figure()
    closingPrice = data['Close']
    closingPrice.index = data['Date']
    ax = closingPrice.plot(kind='line')
    ax.set(ylabel='Closing Price')
    plt.show()
    
    plt.figure()
    N = closingPrice.shape[0]
    Y = pd.Series(closingPrice[1:N].values - closingPrice[:N-1].values, index=closingPrice.index[1:])
    Y.plot(kind='line')
    plt.show()
    
    N = Y.shape[0]
    X = pd.DataFrame( Y[:N-3].values,columns=['t-4'])
    X['t-3'] = Y[1:N-2].values
    X['t-2'] = Y[2:N-1].values
    X['t-1'] = Y[3:N].values
    X = X[:-1]
    X.index = Y[4:].index   
    
    y = Y[4:]
    
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