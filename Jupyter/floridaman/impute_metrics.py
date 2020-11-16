import pandas as pd
import numpy as np
from floridaman import data_cleaning
from floridaman import metrics
from sklearn.impute import KNNImputer

def run_test(df, COLUMN_DROP_THRESHOLD, target_column, neighbors):
    categorical_columns = [col for col in df.columns if df[col].dtypes == 'O']

    for column in df:
        this_percent_null = metrics.getPercentNull(df, column)
        
        if (this_percent_null >= COLUMN_DROP_THRESHOLD):
            del df[column]
        else:
            df.dropna(subset=[column], axis=0, inplace=True)
            
    categorical_columns = [col for col in df.columns if df[col].dtypes == 'O']
    quantitative_columns = [col for col in df.columns if df[col].dtypes == 'float']

    imputer = KNNImputer(n_neighbors=neighbors)
    imputer.fit(df[quantitative_columns])

    source_data = df.copy()
    test_data = df.copy()

    sample_set = test_data.sample(frac=.2).index
    test_data.loc[sample_set, target_column] = np.nan

    test_data['isImputed'] = False
    test_data.loc[sample_set, 'isImputed'] = True

    results = pd.DataFrame(columns=['imputed','source'])

    test_data[quantitative_columns] = imputer.transform(test_data[quantitative_columns])
    results['imputed'] = test_data[target_column][test_data['isImputed'] == True]
    results['source'] = source_data[target_column][test_data['isImputed'] == True]
    results['diff'] = results['imputed'] - results['source']

    return(results['diff'])

def get_stddev(df, COLUMN_DROP_THRESHOLD, target_column, neighbors):
    results = []
    for i in range(1, 8):
        results.append(run_test(df, COLUMN_DROP_THRESHOLD, target_column, neighbors).std())
    return results