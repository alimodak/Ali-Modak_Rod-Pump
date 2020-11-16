import pandas as pd
import numpy as np
from floridaman import data_cleaning
from floridaman import metrics
from sklearn.impute import KNNImputer

def score (df, target_column, COLUMN_DROP_THRESHOLD, neighbors):
    for column in df:
        this_percent_null = metrics.getPercentNull(df, column)
        
        if (this_percent_null >= COLUMN_DROP_THRESHOLD):
            del df[column]
        else:
            df.dropna(subset=[column], axis=0, inplace=True)

    quantitative_columns = [col for col in df.columns if df[col].dtypes == 'float']

    df = df[quantitative_columns]

    imputer = KNNImputer(n_neighbors=neighbors, copy=False)
    imputer.fit(df)

    source_data = df
    test_data = df.copy()

    sample_set = test_data.sample(frac=.2).index
    test_data.loc[sample_set, target_column] = np.nan

    imputer.transform(test_data)
    
    results = pd.DataFrame(columns=['imputed','source'])
    results['imputed'] = test_data.loc[sample_set, target_column]
    results['source'] = source_data.loc[sample_set, target_column]
    results['diff'] = results['imputed'] - results['source']

    return(results)


def score_column (df, target_column, THRESHOLD):
    results = []
    for i in range(1, 8):
        results.append( score(df, target_column, THRESHOLD, 5) )

    results = pd.concat(results)

    print( df[target_column].describe() )
    print('')
    print( "StdDev: " + str(round(results['diff'].std(), 2)) )
    print( results['imputed'].quantile([.25, .5, .75]) )

    df[target_column].hist()
    results['imputed'].hist()