import numpy as np
import pandas as pd
from floridaman import data_cleaning
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import plot_confusion_matrix
from sklearn.metrics import roc_auc_score
from sklearn.metrics import f1_score

n_estimators = [int(x) for x in np.linspace(start = 4, stop = 10, num = 10)]
max_features = ['auto', 'sqrt']
max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
max_depth.append(None)
min_samples_split = [2, 5, 10]
min_samples_leaf = [1, 2, 4]
bootstrap = [True, False]

random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
               'bootstrap': bootstrap}

def train_model(df, threshold, columns):
    candidate_data = data_cleaning.generate_candidate_dataset(df, threshold, threshold, 5)
    train_data = data_cleaning.balance(candidate_data)

    X_train = np.array(train_data[columns])
    y_train = np.array(train_data['FAILURETYPE'])
    X_test = np.array(candidate_data[columns])
    y_test = np.array(candidate_data['FAILURETYPE'])

    rf_model = RandomForestClassifier()
    rf_grid = GridSearchCV(estimator = rf_model, param_grid = random_grid, cv = 8, verbose = 1, n_jobs = -1)
    rf_grid.fit(X_train, y_train)
    
    best_model = rf_grid.best_estimator_

    return f1_score(y_test, best_model.predict(X_test), average='weighted')

if __name__ == "__main__":
    raw_data = data_cleaning.load('null_transformed')

    print( train_model(raw_data, .4, ['PrimarySetpoint','SecondarySetpoint']) )