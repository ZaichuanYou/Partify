import numpy as np
import pandas as pd
import scipy.stats as stats
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC



import warnings
warnings.filterwarnings('ignore')

class rediction_classifier():

    def classifier_selection(self, data):
        self.classifiers = []
        

        for df in data:
            #print(df.head())
            df = df.drop('uri', axis=1)
            df = df.astype(float)
            array = np.array(df)
            models = []
            df = self.cleandata(df)
            array = np.array(df)

            X = array[:, :-1]
            Y = array[:, -1]

            if len(X)<5:
                continue
            
            models.append(('LR', LogisticRegression()))
            models.append(('LDA', LinearDiscriminantAnalysis()))
            models.append(('KNN', KNeighborsClassifier()))
            models.append(('CART', DecisionTreeClassifier()))
            models.append(('NB', GaussianNB()))
            models.append(('SVC', SVC()))

            # evaluate each model in turn
            scoring = 'accuracy'

            max_model = None
            maxnum = 0
            for name, model in models:
                kfold = KFold(n_splits=5, random_state=7, shuffle=True)
                cv_results = cross_val_score(model, X, Y, cv=kfold, scoring=scoring)
                large = cv_results.mean()
                if maxnum < large:
                    maxnum = large
                    max_model = model
                msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
                #print(msg)
                #new_model = name + '-' + str(cv_results.mean())
            # part1 = new_model.split("-")[0]
            # part2 = new_model.split("-")[1]
            self.classifiers.append(max_model.fit(X, Y))
            #print(self.classifiers)
        return self.classifiers


    def predict(self, data, playlist, num):
        data = data.drop('uri', axis=1)
        weight = []
        acc = []
        result_list = []
        
        y = np.ones(len(data))
        for model in self.classifiers:
            y_hat = model.predict(data)
            acc.append(self.acc(y, y_hat))
        acc = np.array(acc)
        for a in acc:
            weight.append(a/acc.sum())
        for list in playlist:
            temp = list.drop('uri', axis=1).to_numpy()
            for song in range(0, len(temp)):
                result = 0
                for classifier in range(0, len(self.classifiers)):
                    result += self.classifiers[classifier].predict([temp[song]])[0]*weight[classifier]
                if result > 0.9:
                    result_list.append(list.iloc[song]["uri"])
                    if len(result_list) == num:
                        return result_list

        
    def acc(self, y, y_hat):
        return (y == y_hat).sum() / y.size

    def cleandata(self, data):
        z_scores = stats.zscore(data)  # calculate z-scores of your dataframe
        abs_z_scores = np.abs(z_scores)
        filtered_entries = (abs_z_scores < 3).all(axis=1)
        new_df = data[filtered_entries]  # we now have deleted the outliers in our data
        dropped_entries = (abs_z_scores >= 3).any(axis=1)
        dropped = data[dropped_entries]
        dropped['label'] = 0
        new_df['label'] = 1
        dataframe = pd.concat([new_df, dropped], ignore_index=True)
        return dataframe
