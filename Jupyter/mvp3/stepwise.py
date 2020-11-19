import numpy as np
import pandas as pd

from floridaman import data_cleaning

from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import RFE
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report

def train(X_train, y_train, X_test, y_test):
    # Create KNN Imputer object
    imputer = KNNImputer()

    # Create scaler object
    scaler = StandardScaler()

    # Create Random Forest Classifier object
    classifier = RandomForestClassifier()

    # Create RFE object
    rfe_classifier = LogisticRegression(max_iter=100, tol=0.1)
    rfe = RFE(rfe_classifier)

    # Combine components into one Pipeline object
    pipeline = Pipeline( steps=[('imputer', imputer), ('scaler', scaler), ('rfe', rfe), ('classifier', classifier)] )

    # Create parameter grid for GridSearchCV
    param_grid = {
        'imputer__n_neighbors': [5],
        'rfe__n_features_to_select': [3, 5, 10, 15, 20, 25],
        'classifier__n_estimators': [int(x) for x in np.linspace(start = 4, stop = 10, num = 4)],
        'classifier__max_features': ['auto', 'sqrt'],
        'classifier__max_depth': [int(x) for x in np.linspace(10, 110, num = 11)],
        'classifier__min_samples_split': [2, 5, 10],
        'classifier__min_samples_leaf': [1, 2, 4],
        'classifier__bootstrap': [True, False]
    }

    # Create and train GridSearchCV object
    gs = GridSearchCV(pipeline, param_grid, verbose=1, n_jobs=-1) # create
    gs.fit(X_train, y_train) # train

    return gs

if __name__ == "__main__":
    raw_data = data_cleaning.load('null_transformed')
    candidate_data = data_cleaning.drop_columns(raw_data, .4, .4)
    train_data = data_cleaning.balance(candidate_data)

    X_train = np.array(train_data[data_cleaning.features(train_data)])
    y_train = np.array(train_data['FAILURETYPE'])

    X_test = np.array(candidate_data[data_cleaning.features(train_data)])
    y_test = np.array(candidate_data['FAILURETYPE'])

    results = train(X_train, y_train, X_test, y_test)

    print(str( classification_report(y_test, results.best_estimator_.predict(X_test)) ) )
    print('')
    print(results.best_params_)
