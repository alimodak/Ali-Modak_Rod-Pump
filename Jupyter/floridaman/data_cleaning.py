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
    SRP = df[df['FAILURETYPE'] == 'Sucker Rod Pump']
    Rods = df[df['FAILURETYPE'] == 'Rods']
    Tubing = df[df['FAILURETYPE'] == 'Tubing']
    maxSize = 0
    normalized_data=0
    
    if len(SRP.index) <len(Rods.index) and len(SRP.index) < len(Tubing.index):
        normalized_data = SRP
        maxSize = len(SRP.index)
    elif len(Tubing.index) < len(Rods.index) and len(Tubing.index) < len(SRP.index):
        normalized_data = Tubing
        maxSize = len(Tubing.index)
    else:
        normalized_data = Rods
        maxSize = len(Rods.index)
    
  
     
    normalized_data = normalize(normalized_data, SRP, maxSize)
    normalized_data = normalize(normalized_data, Tubing, maxSize)

    #shuffle rows in new norm data
    normalized_data = normalized_data.sample(frac=1).reset_index(drop=True)
    
    return normalized_data

def normalize(dfBig, dfSmall, maxSize):
    for i in range(1,maxSize+1):
        randRowNum = random.randint(0,len(dfSmall.index)) #selects randrow in unnorm data
        dfBig = dfBig.append(dfSmall.iloc[randRowNum,:]) #adds that row to norm data
        dfSmall = dfSmall.drop(dfSmall.index[randRowNum]) #drops that row from unnorm data

        #shuffle rows in unnorm data 
        dfSmall = dfSmall.sample(frac=1).reset_index(drop=True)
        
    return dfBig

def balance(this_data):
    # FAILURETYPE key reference
    # Key 2: Tubing
    # Key 1: Sucker Rod Pump
    # Key 0: Rod

    # create a dictionary with value_counts for each failuretype
    frequencies = this_data['FAILURETYPE'].value_counts(normalize=True).to_dict()
    # identify which failuretype has the least number of occurances
    min_key = min(frequencies, key=frequencies.get)
    # extract the count of occurances for the least common failuretype
    min_count = this_data['FAILURETYPE'].value_counts()[min_key]

    # create a list of unique failuretypes present
    unique_types = this_data['FAILURETYPE'].unique()
    # create an empty dataframe
    this_sample = pd.DataFrame()
    # append a random sample of size min_count from each failuretype to the new dataframe
    for this_type in unique_types:
        sample = this_data[ this_data['FAILURETYPE'] == this_type ].sample(n=min_count)
        this_sample = this_sample.append(sample)

    return this_sample
