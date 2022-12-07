from pandas import read_csv
from pandas import set_option
import numpy as np
import pandas as pd
from matplotlib import pyplot
from pandas.plotting import scatter_matrix
import scipy.stats as stats
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from numpy import set_printoptions
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from pandas import read_csv
from numpy import set_printoptions
from pandas import read_csv
from matplotlib import pyplot
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVR
from pandas import read_csv
from matplotlib import pyplot
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_gaussian_quantiles
from sklearn.model_selection import train_test_split
from pickle import load
from pickle import dump


import warnings
warnings.filterwarnings('ignore')

def method(data):
    classifiers = []
    for df in data:
        array = np.array(df)
        length = len(array[0])
        models = []
        X = array[:, 0:length - 1]
        Y = array[:, length - 1]
        df = cleandata(df)
        array = np.array(df)
        models.append(('LR', LogisticRegression()))
        models.append(('LDA', LinearDiscriminantAnalysis()))
        models.append(('KNN', KNeighborsClassifier()))
        models.append(('CART', DecisionTreeClassifier()))
        models.append(('NB', GaussianNB()))
        models.append(('SVC', SVC()))

        # evaluate each model in turn
        scoring = 'accuracy'
        results = []
        max_model = None
        maxnum = 0
        for name, model in models:
            kfold = KFold(n_splits=10, random_state=7, shuffle=True)
            cv_results = cross_val_score(model, X, Y, cv=kfold, scoring=scoring)
            large = cv_results.mean()
            if maxnum < large:
                maxnum = large
                max_model = model
            msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
            print(msg)
            #new_model = name + '-' + str(cv_results.mean())
           # part1 = new_model.split("-")[0]
           # part2 = new_model.split("-")[1]
        classifiers.append(max_model)
        print(classifiers)

    for model in classifiers:
        weight = []
        results = []
        models = model
        model.fit(X, Y)
        # save the model to disk
        dump(models, open(filename, 'wb'))
        # some time later...
        # load the model from disk
        loaded_model = load(open(filename, 'rb'))
        result = loaded_model.score(X_test, Y_test)
        results.append(result)
        for result in results:
            w_value = result / sum(results)
            weight.append(w_value)
        print(weight)

def cleandata(data):
    df = data
    z_scores = stats.zscore(df)  # calculate z-scores of your dataframe
    abs_z_scores = np.abs(z_scores)
    filtered_entries = (abs_z_scores < 3).all(axis=1)
    new_df = df[filtered_entries]  # we now have deleted the outliers in our data
    dropped_entries = (abs_z_scores >= 3).any(axis=1)
    dropped = df[dropped_entries]
    dropped['label'] = 0
    new_df['label'] = 1
    dataframe = pd.concat([new_df, dropped], ignore_index=True)
    return dataframe


if __name__ == '__main__':
    filename = 'C:/Users/29083/Desktop/data.csv'
    file = pd.read_csv(filename)
    method([file])
