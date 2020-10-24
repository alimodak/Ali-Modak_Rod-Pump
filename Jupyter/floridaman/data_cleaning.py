import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import KNNImputer
from floridaman.metrics import getPercentNull
import numpy as np
from numpy import random

def load(source):
    if (source=='null_transformed'):
        return pd.read_csv('floridaman/data/jmm_raw.csv', parse_dates=['lifetime_start','lifetime_end'])
    else:
        return

def preprocess(df):
    # Calculate lifetime from lifetime_start and lifetime_end
    df['lifetime'] = (df['lifetime_end'] - df['lifetime_start']).dt.days

    # Remove procedural and redundant columns
    del df['FAILSTART']
    del df['NODEID']
    del df['IDWELL']
    del df['REPORTTO']
    del df['tbguid']
    del df['IDRECJOBPULL']

    # Remove rows corresponding to columns 
    df = df[df['FAILURETYPE'].notnull()]

def encode(df, column):
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column])
    
    # classes = list(le.classes_)
    # print(column + ":")
    # for key in range(len(classes)):
        # print('[' + str(key) + '] ' + str(classes[key]))
    # print('')
    return df

def generate_candidate_dataset(data_in, COLUMN_DROP_THRESHOLD, COLUMN_IMPUTE_THRESHOLD, neighbors):
    this_data = data_in.copy()
    categorical_columns = [col for col in this_data.columns if this_data[col].dtypes == 'O']
    quantitative_columns = [col for col in this_data.columns if this_data[col].dtypes == 'float']

    for column in this_data:
        this_percent_null = getPercentNull(this_data, column)

        if (this_percent_null >= COLUMN_DROP_THRESHOLD):
            del this_data[column]
        elif (this_percent_null >= COLUMN_IMPUTE_THRESHOLD):
            this_data.dropna(subset=[column], axis=0, inplace=True)
        else:
            if (column in categorical_columns):
                this_data.dropna(subset=[column], axis=0, inplace=True)

    categorical_columns = [col for col in this_data.columns if this_data[col].dtypes == 'O']
    quantitative_columns = [col for col in this_data.columns if this_data[col].dtypes == 'float']

    imputer = KNNImputer(n_neighbors=neighbors)
    imputer.fit(this_data[quantitative_columns])
    this_data[quantitative_columns] = imputer.transform(this_data[quantitative_columns])

    for column in this_data:
        if (column in categorical_columns):
            encode(this_data, column)
    
    return this_data

def features(df):
    features = list(df)
    to_remove = ['FAILURETYPE', 'roduid', 'UWI', 'lifetime_start', 'lifetime_end']
    for column in to_remove:
        try:
            features.remove(column)
        except:
            pass
    return features





def fullNormData(df):
    SRP = pd.DataFrame(raw_data[raw_data['FAILURETYPE'] == 'Sucker Rod Pump'])
    Rods = pd.DataFrame(raw_data[raw_data['FAILURETYPE'] == 'Rods'])
    Tubing = pd.DataFrame(raw_data[raw_data['FAILURETYPE'] == 'Tubing'])
    normalized_data = Rods
    maxSize = len(Rods.index)
    

    def normalize(df,maxSize):
        global normalized_data
        for i in range(1,maxSize+1):
            randRowNum = random.randint(0,len(df.index))
            normalized_data = normalized_data.append(df.iloc[randRowNum,:])
            df = df.drop(df.index[randRowNum])

            #shuffle rows in df
            df = df.sample(frac=1).reset_index(drop=True)
     
    normalize(SRP, maxSize)
    normalize(Tubing, maxSize)

    #shuffle rows in new df
    normalized_data.sample(frac=1).reset_index(drop=True)
    
    return normalized_data