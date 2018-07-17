import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report
from statistics import mode
import re
from xgboost import XGBClassifier

df = pd.read_csv('E:\Machine Learning\XGBoost\h1b_kaggle.csv')

#exploring the data
df.info()
df.head()
df.describe()

#reading the classes in the target variable
df['CASE_STATUS'].unique()
df.head(10)

#converting the entire dataset into only 2 classes certified and denied
import warnings
warnings.filterwarnings("ignore")
df.CASE_STATUS[df['CASE_STATUS']=='REJECTED'] = 'DENIED'
df.CASE_STATUS[df['CASE_STATUS']=='INVALIDATED'] = 'DENIED'
df.CASE_STATUS[df['CASE_STATUS']=='PENDING QUALITY AND COMPLIANCE REVIEW - UNASSIGNED'] = 'DENIED'
df.CASE_STATUS[df['CASE_STATUS']=='CERTIFIED-WITHDRAWN'] = 'CERTIFIED'

#dropping the withdrawn class entries
df.EMPLOYER_NAME.describe()
df = df.drop(df[df.CASE_STATUS == 'WITHDRAWN'].index)

## Storing non null in df w.r.t. case status
df = df[df['CASE_STATUS'].notnull()]
print(df['CASE_STATUS'].value_counts())

##check count of NAN
count_nan = len(df) - df.count()
print(count_nan)

#replacing missing values with mode value for employer_name
df['EMPLOYER_NAME'] = df['EMPLOYER_NAME'].fillna(df['EMPLOYER_NAME'].mode()[0])

assert pd.notnull(df['EMPLOYER_NAME']).all().all()

##to check the percentile in wages
print(np.nanpercentile(df.PREVAILING_WAGE,98))
df.PREVAILING_WAGE.median() 

## replacing min and max with 2 and 98 percentile
df.loc[df.PREVAILING_WAGE < 34029, 'PREVAILING_WAGE']= 34029
df.loc[df['PREVAILING_WAGE'] > 138703, 'PREVAILING_WAGE']= 138703
df.PREVAILING_WAGE.fillna(df.PREVAILING_WAGE.mean(), inplace = True)

## Filling na in JOB_TITLE and FULL_TIME_POSITION with mode
df['JOB_TITLE'] = df['JOB_TITLE'].fillna(df['JOB_TITLE'].mode()[0])
df['FULL_TIME_POSITION'] = df['FULL_TIME_POSITION'].fillna(df['FULL_TIME_POSITION'].mode()[0])
df['SOC_NAME'] = df['SOC_NAME'].fillna(df['SOC_NAME'].mode()[0])

#analysis the Full Time Position column
foo1 = df['FULL_TIME_POSITION']=='Y'
foo2 = df['CASE_STATUS']=='CERIFIED'
print(len(df[foo1])/len(df))

fooy = df.FULL_TIME_POSITION[df['FULL_TIME_POSITION']=='Y'].count()
foox = df.CASE_STATUS[df['CASE_STATUS']=='CERIFIED'].count()
print(fooy/df.FULL_TIME_POSITION.count())

# Dropping lat and lon columns
df = df.drop('lat', axis = 1)
df = df.drop('lon', axis = 1)

#   
df['NEW_EMPLOYER'] = np.nan
df.shape

warnings.filterwarnings("ignore")

df['EMPLOYER_NAME'] = df['EMPLOYER_NAME'].str.lower()
df.NEW_EMPLOYER[df['EMPLOYER_NAME'].str.contains('university')] = 'university'
df['NEW_EMPLOYER']= df.NEW_EMPLOYER.replace(np.nan, 'non university', regex=True)

# Creating occupation and mapping the values
warnings.filterwarnings("ignore")

df['OCCUPATION'] = np.nan
df['SOC_NAME'] = df['SOC_NAME'].str.lower()
df.OCCUPATION[df['SOC_NAME'].str.contains('computer','programmer')] = 'computer occupations'
df.OCCUPATION[df['SOC_NAME'].str.contains('software','web developer')] = 'computer occupations'
df.OCCUPATION[df['SOC_NAME'].str.contains('database')] = 'computer occupations'
df.OCCUPATION[df['SOC_NAME'].str.contains('math','statistic')] = 'Mathematical Occupations'
df.OCCUPATION[df['SOC_NAME'].str.contains('predictive model','stats')] = 'Mathematical Occupations'
df.OCCUPATION[df['SOC_NAME'].str.contains('teacher','linguist')] = 'Education Occupations'
df.OCCUPATION[df['SOC_NAME'].str.contains('professor','Teach')] = 'Education Occupations'
df.OCCUPATION[df['SOC_NAME'].str.contains('school principal')] = 'Education Occupations'
df.OCCUPATION[df['SOC_NAME'].str.contains('medical','doctor')] = 'Medical Occupations'
df.OCCUPATION[df['SOC_NAME'].str.contains('physician','dentist')] = 'Medical Occupations'
df.OCCUPATION[df['SOC_NAME'].str.contains('Health','Physical Therapists')] = 'Medical Occupations'
df.OCCUPATION[df['SOC_NAME'].str.contains('surgeon','nurse')] = 'Medical Occupations'
df.OCCUPATION[df['SOC_NAME'].str.contains('psychiatr')] = 'Medical Occupations'
df.OCCUPATION[df['SOC_NAME'].str.contains('chemist','physicist')] = 'Advance Sciences'
df.OCCUPATION[df['SOC_NAME'].str.contains('biology','scientist')] = 'Advance Sciences'
df.OCCUPATION[df['SOC_NAME'].str.contains('biologi','clinical research')] = 'Advance Sciences'
df.OCCUPATION[df['SOC_NAME'].str.contains('public relation','manage')] = 'Management Occupation'
df.OCCUPATION[df['SOC_NAME'].str.contains('management','operation')] = 'Management Occupation'
df.OCCUPATION[df['SOC_NAME'].str.contains('chief','plan')] = 'Management Occupation'
df.OCCUPATION[df['SOC_NAME'].str.contains('executive')] = 'Management Occupation'
df.OCCUPATION[df['SOC_NAME'].str.contains('advertis','marketing')] = 'Marketing Occupation'
df.OCCUPATION[df['SOC_NAME'].str.contains('promotion','market research')] = 'Marketing Occupation'
df.OCCUPATION[df['SOC_NAME'].str.contains('business','business analyst')] = 'Business Occupation'
df.OCCUPATION[df['SOC_NAME'].str.contains('business systems analyst')] = 'Business Occupation'
df.OCCUPATION[df['SOC_NAME'].str.contains('accountant','finance')] = 'Financial Occupation'
df.OCCUPATION[df['SOC_NAME'].str.contains('financial')] = 'Financial Occupation'
df.OCCUPATION[df['SOC_NAME'].str.contains('engineer','architect')] = 'Architecture & Engineering'
df.OCCUPATION[df['SOC_NAME'].str.contains('surveyor','carto')] = 'Architecture & Engineering'
df.OCCUPATION[df['SOC_NAME'].str.contains('technician','drafter')] = 'Architecture & Engineering'
df.OCCUPATION[df['SOC_NAME'].str.contains('information security','information tech')] = 'Architecture & Engineering'
df['OCCUPATION']= df.OCCUPATION.replace(np.nan, 'Others', regex=True)

## Splitting city and state and capturing state in another variable
df['state'] = df.WORKSITE.str.split('\s+').str[-1]

print(df.head())

#converting classes to binary 0 & 1
from sklearn import preprocessing
class_mapping = {'CERTIFIED':0, 'DENIED':1}
df["CASE_STATUS"] = df["CASE_STATUS"].map(class_mapping)from sklearn import preprocessing
class_mapping = {'CERTIFIED':0, 'DENIED':1}
df["CASE_STATUS"] = df["CASE_STATUS"].map(class_mapping)

print(df.head())

#identify job title unique values
test1 = pd.Series(df['JOB_TITLE'].ravel()).unique()
print(pd.DataFrame(test1))

# dropping these columns
df = df.drop('EMPLOYER_NAME', axis = 1)
df = df.drop('SOC_NAME', axis = 1)
df = df.drop('JOB_TITLE', axis = 1)
df = df.drop('WORKSITE', axis = 1)
df = df.drop('CASE_ID', axis = 1)

df1 = df.copy()

df1[['CASE_STATUS', 'FULL_TIME_POSITION', 'YEAR','NEW_EMPLOYER','OCCUPATION','state']] = df1[['CASE_STATUS', 'FULL_TIME_POSITION', 'YEAR','NEW_EMPLOYER','OCCUPATION','state']].apply(lambda x: x.astype('category'))

df1.info()

X = df.drop('CASE_STATUS', axis=1)
y = df.CASE_STATUS

seed = 7
test_size = 0.40
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=seed)
X_train.columns

Index(['FULL_TIME_POSITION', 'PREVAILING_WAGE', 'YEAR', 'NEW_EMPLOYER',
       'OCCUPATION', 'state'],
      dtype='object')
print(X_train.isnull().sum())

#encoding the data to be used for XGBoost
X_train_encode = pd.get_dummies(X_train)
X_test_encode = pd.get_dummies(X_test)
y_train.head()

#converting categorical variables to numeric
train_X = X_train_encode.as_matrix()
train_y = y_train.as_matrix()

import xgboost
gbm=xgboost.XGBClassifier(max_features='sqrt', subsample=0.8, random_state=10)

#tuning parameters
from sklearn.model_selection import GridSearchCV
parameters = [{'n_estimators': [10, 100]},
              {'learning_rate': [0.1, 0.01, 0.5]}]
grid_search = GridSearchCV(estimator = gbm, param_grid = parameters, scoring='accuracy', cv = 3, n_jobs=-1)
grid_search = grid_search.fit(train_X, train_y) 

gbm=xgboost.XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
       colsample_bytree=1, gamma=0, learning_rate=0.5, max_delta_step=0,
       max_depth=3, max_features='sqrt', min_child_weight=1, missing=None,
       n_estimators=100, n_jobs=1, nthread=None,
       objective='binary:logistic', random_state=10, reg_alpha=0,
       reg_lambda=1, scale_pos_weight=1, seed=None, silent=True,
       subsample=0.8).fit(train_X, train_y)
y_pred = gbm.predict(X_test_encode.as_matrix())
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))





