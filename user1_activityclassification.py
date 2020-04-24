# -*- coding: utf-8 -*-
"""User1_activityClassification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/100-TmGQiSJmnH-fs1DgZ700iw8b2LlXA
"""

'''
Created on 13-Apr-2020

@author: joel peter
'''

from google.colab import files
uploaded = files.upload()

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import io
import matplotlib.pyplot as plt
import numpy as np
import statistics
import seaborn as sns
import missingno as mno
from sklearn import linear_model
import datetime
# %matplotlib inline
from operator import itemgetter
from itertools import groupby
import statsmodels.api as sm

feat_cleaning_df = pd.read_csv(io.BytesIO(uploaded['user1_datapreprocessing.csv']), encoding = "ISO-8859-1", parse_dates = ['date'])

"""Lifelogging is a wearable camera. User turns it off while sleeping and turns it on once he/she is awake. Take the img id, if its null for more than 4 or 5 hours, then user is considered to be sleeping."""

feat_cleaning_df['Sleep_det'] = feat_cleaning_df['img00_id'].apply(lambda x: 1 if not pd.isnull(x) else 0)

#feat_cleaning_df.info()
feat_cleaning_df.head()

"""See the sleep distribution"""

sleep_counter = 0
index_list = []
ranges = []
for index, row in feat_cleaning_df.iterrows():
    value = row['img00_id']
    if value is np.nan:
        index_list.append(index)

print(type(index_list[0]))

"""use lambda functions to get the sleep index and waking up index"""

for key, group in groupby(enumerate(index_list), lambda  value: value[0] - value[1]):   
    group = list(map(itemgetter(1), group))
    ranges.append((group[0],group[-1]))

print(ranges)

sleep_index = []
for tup in ranges:
  first_index = tup[0]
  last_index = tup[1]
  diff = last_index - first_index
  if diff > 300:
    for i in range(first_index, last_index + 1):
      sleep_index.append(i)

for index in sleep_index:
    feat_cleaning_df.loc[index, 'activity'] = 'Sleeping'

feat_cleaning_df.head()

"""Look at the different location the user has travelled and segregate into appropriate destination"""

work_location = ['dcu engineering building', 'dcu engineering building', 'dcu school of computing', 'the helix', "st patrick's college, dublin", 'work',
                 'office', 'leman solicitors', 'tsb','dcu']
shopping = ['store', 'shopping', 'shop', 'centre', 'retail', 'stores', 'supervalu', 'toys']
restraunt = ['hotel', 'bakery', 'pub', 'bar', 'restaurant', 'b&q', 'barbecue', 'coffee', 'cafe', 'tea', 'rooms', 'inn', 'restrant', "angelina's"]
relaxing = ['park', 'drive', 'port', 'harbour', 'howth']
home = ['home', 'house']
terminal = ['airport', 'terminal', 'rail', 'railway', 'bus', 'station']

for index, row in feat_cleaning_df.iterrows():
    activity = row['activity']
    place = row['name'] 
    if activity == 'Sleeping' and place is np.nan:
        feat_cleaning_df.loc[index, 'name'] = 'Home'

"""Convert object type column into String format"""

feat_cleaning_df.name = feat_cleaning_df.name.fillna(value="")
feat_cleaning_df['name'] = feat_cleaning_df['name'].astype(str)
feat_cleaning_df.activity = feat_cleaning_df.activity.fillna(value="")
feat_cleaning_df['activity'] = feat_cleaning_df['activity'].astype(str)
#eda_df.to_csv(r'new.csv',index = None, header=True)

"""We are starting the analysis from the 2nd day"""

analysis_df = feat_cleaning_df.iloc[1382:]     
analysis_df.reset_index(drop = True, inplace = True)

"""This is to identify where the lifelogger is travelling. Based on the name column in our dataset, which has the location, we impute values into activity"""

previous_place = ''
previous_index = 0
destination = ''
count = 0
for index, row in analysis_df.iterrows():
  activity = row['activity']
  place = row['name']
  place = place.lower()
  if place is not "" and place != previous_place:
    for loc in work_location:
      if loc in place:
        destination = 'Work'
        break
            
    for loc in shopping:
      if loc in place:
        destination = 'Shop'
        break

    for loc in restraunt:
      if loc in place:
        destination = 'Cafe/Restaurant'
        break

    for loc in home:
      if loc in place:
        destination = 'Home'
        break
      
    for loc in relaxing:
      if loc in place:
        destination = 'Relax'
        break

    for loc in terminal:
      if loc in place:
        destination = 'Terminal'
        break

    if destination == '':
      destination = 'Uncategorized destination'

    analysis_df.loc[previous_index + 1: index - 1, 'activity_new'] = 'Travelling to ' + destination
    
    
  destination = ''
  if place is not "":
    previous_index = index
    previous_place = place

analysis_df.head()

for index, row in analysis_df.iterrows():
  activity = row['activity_new']
  old_activity = row['activity']
  if old_activity == 'transport':
    analysis_df.loc[index, 'activity'] = activity

analysis_df['activity'] = analysis_df['activity'].fillna(value="")
analysis_df['activity'] = analysis_df['activity'].astype(str)

for index, row in analysis_df.iterrows():
  old_activity = row['activity']
  place = row['name']
  place = place.lower()
  old_activity = old_activity.lower()
  if old_activity is "":
    for loc in work_location:
      if loc in place:
        activity = 'working'
        break
                
    for loc in shopping:
      if loc in place:
        activity = 'Shopping'
        break
            
    for loc in restraunt:
      if loc in place:
        activity = 'Eating/Recreational'
        break
            
    for loc in home:
      if loc in place:
        activity = 'Working/Eating/Relaxing?'
        break
            
    for loc in relaxing:
      if loc in place:
        activity = 'Recreational'
        break
                    
    for loc in terminal:
      if loc in place:
        activity = 'At travel Station'
        break
        
    if activity == '':
      activity = 'Unrecognised'
        
    analysis_df.loc[index, 'activity'] = activity
    activity= ''

for index, row in analysis_df.iterrows():
  activity = row['activity']
  steps = row['steps']
  distance = row['distance']

  if steps > 50 and distance > 0.0:
    analysis_df.loc[index, 'activity'] = 'Walking'

analysis_df.info()

analysis_df.drop(columns= ['utc_time', 'local_time', 'time_zone', 'img00_id', 'new_row', 'Sleep_det', 'activity_new'], inplace = True)

from google.colab import files
analysis_df.to_csv('user1_cleaned.csv', date_format='%Y-%m-%d %H:%M:%S', index = False) 
files.download('user1_cleaned.csv')

X = analysis_df[['steps','calories']] # here we have 2 variables for multiple regression. If you just want to use one variable for simple linear regression, then use X = df['Interest_Rate'] for example.Alternatively, you may add additional variables within the brackets
Y = analysis_df['heart_rate_imputed']
 
# with sklearn
regr = linear_model.LinearRegression()
regr.fit(X, Y)

print('Intercept: \n', regr.intercept_)
print('Coefficients: \n', regr.coef_)

# prediction with sklearn
steps = 10
calories = 4.6939997673
print ('Predicted heart_rate', regr.predict([[steps ,calories]]))

# with statsmodels
X = sm.add_constant(X) # adding a constant
 
model = sm.OLS(Y, X).fit()
predictions = model.predict(X) 
 
print_model = model.summary()
print(print_model)