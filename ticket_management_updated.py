# -*- coding: utf-8 -*-
"""TICKET_MANAGEMENT_updated.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1oSeNbjKC8oveaozV5JWLCe3xV3kALCT8

#Client: ABC Tech | Category: ITSM - ML Project Ref: PM-PR-0012

#Business Case:


---


ABC Tech is an mid-size organisation operation in IT-enabled business
segment over a decade. On an average ABC Tech receives 22-25k IT
incidents/tickets , which were handled to best practice ITIL framework
with incident management , problem management, change management
and configuration management processes. These ITIL practices attained
matured process level and a recent audit confirmed that further
improvement initiatives may not yield return of investment.



---


ABC Tech management is looking for ways to improve the incident
management process as recent customer survey results shows that
incident management is rated as poor.
Machine Learning as way to improve ITSM processes
ABC Tech management recently attended Machine Learning conference on
ML for ITSM.
Machine learning looks prospective to improve ITSM processes through
prediction and automation. They came up with 4 key areas, where ML can
help ITSM process in ABC Tech.
1. Predicting High Priority Tickets: To predict priority 1 & 2 tickets, so
that they can take preventive measures or fix the problem before
it surfaces.
2. Forecast the incident volume in different fields , quarterly and
annual. So that they can be better prepared with resources and
technology planning.
3. Auto tag the tickets with right priorities and right departments so
that reassigning and related delay can be reduced.
4. Predict RFC (Request for change) and possible failure /
misconfiguration of ITSM assets.

#importing neccessory libraries
"""

#basic modules
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import datetime
import pickle

import warnings
warnings.filterwarnings('ignore')

#sklearn modules
##data preprocessing
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

##model creation
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier,BaggingClassifier,GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from xgboost import XGBClassifier

from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.arima.model import ARIMA


#model evaluation
from sklearn.metrics import confusion_matrix,classification_report,ConfusionMatrixDisplay,f1_score,recall_score,accuracy_score

encoder=LabelEncoder()

"""#connecting to database"""

!pip install mysql-connector-python

import mysql.connector

connection = mysql.connector.connect(
    host="18.136.157.135",
    user="dm_team",
    password="DM!$Team@&27920!",
    database="project_itsm"
)

"""#basic checks"""

query = 'select * from dataset_list'
df=pd.read_sql(query,connection)

df = df.replace('', pd.NA)

pd.set_option('display.max_columns',None)

df.head()

exclude_columns =['CI_Name','CI_Subcat','WBS','Incident_ID','number_cnt','KB_number','Open_Time','Reopen_Time','Resolved_Time',
      'Close_Time','Handle_Time_hrs','Related_Interaction','No_of_Related_Incidents','No_of_Related_Changes','Related_Change']
print(len([column for column in df.columns if column not in exclude_columns]))
print('\n')
print([column for column in df.columns if column not in exclude_columns])

"""#EDA"""

pl_no=1
plt.figure(figsize=(10,18))
for i in [column for column in df.columns if column not in exclude_columns]:

  plt.subplot(5,2,pl_no)
  sns.countplot(x=i,data=df)
  plt.xlabel(i)
  plt.xticks(rotation=90)
  pl_no+=1
plt.tight_layout()

"""
##Insight-1
---


* in `CI_cat`, that is in the department section of the dataset, it is found that the `application` is having more count compared to others
* Th `Status` of almost all of tickets is in closed state
* In the `impact`,`urgency` and `priorty` columns most of the tickets are having imapct and urgency of either 4 or 5
* and the most of the tickets are belonging to the `incident` category
* `No_of_Reassignments` column indicating that most of the tickets solved at `first assignment` and also `some entries are there having reassigned many times`
* `others` and `software` were indicated as the major closure code after the tikcet resloving


---


"""

df.info()

"""

---

* **converting the `null count to the percentage` of the null values present for  better handling purpuse**


---


"""

null_df=pd.DataFrame((df.isnull().sum()/len(df))*100,columns=['per'])
null_df['count']=df.isnull().sum()
null_df

"""

---

**droppping the `columns which are above 50% `null values**



---

"""

null_df[null_df['per']>50]

df.drop(null_df[null_df['per']>50].index,axis=1,inplace=True)

for i in df.columns:
    if df[i].dtype=='object':

        print(f'{i} {len(df[i].unique())}')
        print('----'*5)

"""#check for unique values

---



checking all the unique values of categorical columns

fixing the number 66 after knowing the maximum length of discrete columns


---





"""

for i in df.columns:
    if df[i].dtype=='object':
        if len(df[i].unique())<66:
            print(f'{i} -----> {df[i].unique()}')
            print('----'*10)

"""#data preprocessing column by column



---


* ML algorithms will work well if first undertood the data well, so im doing this way to understand the data well to preprocess the well

* preprocessing the data column by column for better cleaning of data

* in the preprocessing the stages follwing these steps
    1. null value imputation
    2. label encoding
    3. force typecating
    4. dropping the unnessesory columns

    and other required preprocessing steps


---



---

## df['CI_Name']

---



---


*  as name doesnot impact on ticket priority dropping the name column

---
"""

df.drop('CI_Name',axis=1,inplace=True)

"""## df['CI_Cat']"""

df['CI_Cat'].value_counts()

df['CI_Cat'].isnull().sum()

df.loc[df['CI_Cat'].isnull(),'CI_Cat']='application'

df['CI_Cat'].value_counts()

"""*  transforming the columns from categorical columns to numerical columns using `label_encoder`"""

df['CI_Cat']=encoder.fit_transform(df['CI_Cat'])

df.head()

"""## df['CI_Subcat']"""

df['CI_Subcat'].unique()

df['CI_Subcat'].isnull().sum()

df['CI_Subcat'].mode()

"""*  there were 111 null values present this columns replacing those with mode i.e. `server based application`"""

df.loc[df['CI_Subcat'].isnull(),'CI_Subcat']=df['CI_Subcat'].mode()[0]

df['CI_Subcat'].isnull().sum()

"""*  using `lable_encoder` to transform categorical to numerical columns"""

df['CI_Subcat']=encoder.fit_transform(df['CI_Subcat'])

df.head()

"""## df['WBS']"""

len(df['WBS'].unique())

"""* extracting the unique numbers of the WBS system"""

df['WBS']=df['WBS'].apply(lambda x: x[-3:])

df['WBS']

df['WBS']=df['WBS'].astype(int)

df.head()

"""## df['Incident_ID']"""

len(df['Incident_ID'].unique())

"""* there are `46606` unique values in this column and it carries no weight to data  so dropping the column"""

df.drop('Incident_ID',axis=1,inplace=True)

df.head()

"""## df['Status']"""

df['Status'].unique()

"""*  using label encoder to convert the categorical columns to numerical columns

"""

df['Status'].isnull().sum()

df['Status']=encoder.fit_transform(df['Status'])

df.head()

"""## df['Impact']"""

df['Impact'].value_counts()

df['Impact'].mode()[0]

"""*  replacing the null values with mode of the column i.e 4"""

df.loc[df['Impact']=='NS','Impact']=df['Impact'].mode()[0]

df.loc[df['Impact']=='NS']

df['Impact'].dtype

df['Impact']=df['Impact'].astype(int)

df['Impact'].unique()

"""## df['Urgency']"""

df['Urgency'].value_counts()

"""*  as only 1 entry there in data dropping the column"""

df.drop(df.loc[df['Urgency']=='5 - Very Low'].index,axis=0,inplace=True)

df['Urgency'].value_counts()

df['Urgency']=df['Urgency'].astype(int)

df['Urgency'].unique()

df.shape

df.head()

"""## df['Priority']"""

df['Priority'].unique()

df['Priority'].value_counts()

"""*  replacing the null values with mode"""

df['Priority'].mode()

df.loc[df['Priority']=='NA','Priority']=df['Priority'].mode()[0]

df['Priority']=df['Priority'].astype(int)

df.head()

"""##df['number_cnt']"""

df['number_cnt']=df['number_cnt'].astype(float)

"""## df['Category']"""

df['Category'].unique()

"""*  transforming the catergorical columns to numerical columns"""

df['Category']=encoder.fit_transform(df['Category'])

df.head()

"""## df['Alert_Status']"""

df['Alert_Status'].unique()

df['Alert_Status'].value_counts()

"""
*  as almost all the columns are in `closed` state dropping the columns"""

df.drop('Alert_Status',axis=1,inplace=True)

df.head()

"""## df['KB_number']"""

len(df['KB_number'].unique())

"""*  extracting the last 4 numbers of column"""

df['KB_number']=df['KB_number'].apply(lambda x: x[-4:])

df['KB_number']=df['KB_number'].astype(int)

df.head()

len(df['KB_number'].unique())

"""## df['No_of_Reassignments']"""

len(df['No_of_Reassignments'].unique())

df['No_of_Reassignments'].mode()

df['No_of_Reassignments'].isnull().sum()

"""*  replacing the null values with mode i.e 0"""

df.loc[df['No_of_Reassignments'].isnull(),'No_of_Reassignments']=df['No_of_Reassignments'].mode()[0]

df['No_of_Reassignments'].isnull().sum()

df['No_of_Reassignments']=df['No_of_Reassignments'].astype(int)

df.head()

"""## df['Open_Time']"""

df['Open_Time'].isnull().sum()

"""*  converting the open time column to datetime format"""

df['Open_Time']=pd.to_datetime(df['Open_Time'])

df.head()

"""## df['Resolved_Time']"""

df['Resolved_Time']=pd.to_datetime(df['Resolved_Time'])

df.head()

df['Resolved_Time'].isnull().sum()

df['Resolved_Time'].mode()[0]

df.loc[df['Resolved_Time'].isnull(),'Resolved_Time']=df['Resolved_Time'].mode()[0]

df['Resolved_Time'].isnull().sum()

df['Resolved_Time']=pd.to_datetime(df['Resolved_Time'])

df.head()

"""## df['Close_Time']"""

df['Close_Time'].isnull().sum()

df['Close_Time']=pd.to_datetime(df['Close_Time'])

df.head()

"""## df['Handle_Time_hrs']

*   manually creating the `handle_time_hrs` as the given `handle_time_hrs` is not carrying any meaningfull information
*  converting the difference days to hours taken
"""

df.drop('Handle_Time_hrs',axis=1,inplace=True)

df['Handle_Time_hrs_conv']=abs(df['Close_Time']-df['Open_Time'])

a=[]
for i in df['Handle_Time_hrs_conv'].index:
    a.append((df['Handle_Time_hrs_conv'][i].total_seconds())/3600)

df['Handle_Time_hrs_conv']=a

df.head()

"""## df['Closure_Code']

* as the closure code will not determine the ticket priority and importance as its done at the posterior stage of ticket resolving
"""

df.drop('Closure_Code',axis=1,inplace=True)

df.head()

"""## df['No_of_Related_Interactions']"""

df['No_of_Related_Interactions'].isnull().sum()

len(df['No_of_Related_Interactions'].unique())

df['No_of_Related_Interactions'].mode()

"""*  replacing the null values with mode"""

df.loc[df['No_of_Related_Interactions'].isnull(),'No_of_Related_Interactions']=df['No_of_Related_Interactions'].mode()[0]

df['No_of_Related_Interactions'].isnull().sum()

df['No_of_Related_Interactions']=df['No_of_Related_Interactions'].astype(int)

df.head()

"""## df['Related_Interaction']"""

len(df['Related_Interaction'].unique())

df.drop('Related_Interaction',axis=1,inplace=True)

"""## Preprocessed dataset for machine learning"""

df.head()

df.shape

df['Resolved_Time'].dtype

"""#Outlier Handling

"""

pl_no=1
plt.figure(figsize=(10,7))
for i in [column for column in df.columns if df[column].dtype!='<M8[ns]']:
  plt.subplot(4,4,pl_no)
  sns.boxplot(x=i,data=df)
  pl_no+=1
  plt.xlabel(i)
plt.tight_layout()

plt.figure(figsize=(12,8))
sns.heatmap(df.drop('Priority',axis=1).corr(),annot=True,cmap='ocean')

df.drop('Impact',axis=1,inplace=True)

df.head()

"""# Task 1
1. Predicting High Priority Tickets: To predict priority 1 & 2 tickets, so that they can take preventive measures or fix the problem before it surfaces.
"""

data=df.copy()

data.head()

# sns.pairplot(data=data)

"""*  as we already used these columns and converted to `handle_time_hrs` dropping these columns"""

data.isnull().sum()

data=data.drop(['Open_Time','Resolved_Time','Close_Time'],axis=1)

data.head()

data.info()

scaler=MinMaxScaler()

X=data.drop(['Priority','Urgency'],axis=1)

X.head()

y=data['Priority'].map({1:1,2:1,3:0,4:0,5:0})

y.value_counts()

"""##train test split"""

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42,stratify=y)

print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)

"""##scaling"""

# X_train_scaled=scaler.fit_transform(X_train)
# X_test_scaled=scaler.transform(X_test)

# X_train_scaled=pd.DataFrame(X_train_scaled,columns=X_train.columns)
# X_train_scaled.head()

# X_test_scaled=pd.DataFrame(X_test_scaled,columns=X_test.columns)
# X_test_scaled.head()

"""##function for model selection task1

##Logic behind the function


---


 1. first creating a dictionary with the name model_summary and initiating with null values with proper keys

 2. function called `model_selection` will take model as parameter
 3.initially the model will be `initiated` within the function and will be `stored in the variable called model`
 4. model will be `fitted on x_train and y_train`
 5.model will `first predict on test data`
 6.after prediction all the evaluation  `metric values will be appended to dictionary` with corresponding key values.
 7.then it will `print the confusion matrix and classification report` of that model
 8.the same `steps will also the performed` on train data
 ---
"""

model_summary_1={'model_name_train':[],'f1_score_train':[],'recall_score_train':[],'accuracy_score_train':[],
               'model_name_test':[],'f1_score_test':[],'recall_score_test':[],'accuracy_score_test':[]}

def model_selction_1(model):

    #model initialization ,fitting and predicting
    print(model)
    model=model()
    model.fit(X_train,y_train)
    model_pred=model.predict(X_test)

    #appending the metrics to the dictionary created
    model_summary_1['model_name_test'].append(model.__class__.__name__)
    model_summary_1['f1_score_test'].append(f1_score(y_test,model_pred,average='macro'))
    model_summary_1['recall_score_test'].append(recall_score(y_test,model_pred,average='macro'))
    model_summary_1['accuracy_score_test'].append(accuracy_score(y_test,model_pred))

    #printing the confusion metrics and classification report
    print('metrics on test data')
    print(confusion_matrix(y_test,model_pred))
    print('\n')
    print(classification_report(y_test,model_pred))

    #predictions on train data
    model_pred1=model.predict(X_train)

    #appending the metrics to the dictionary created
    model_summary_1['model_name_train'].append(model.__class__.__name__)
    model_summary_1['f1_score_train'].append(f1_score(y_train,model_pred1,average='macro'))
    model_summary_1['recall_score_train'].append(recall_score(y_train,model_pred1,average='macro'))
    model_summary_1['accuracy_score_train'].append(accuracy_score(y_train,model_pred1))

    #printing the confusion metrics and classification report
    print('metrics on train data')
    print(confusion_matrix(y_train,model_pred1))
    print('\n')
    print(classification_report(y_train,model_pred1))
    print('==='*10)

models=[LogisticRegression,DecisionTreeClassifier,RandomForestClassifier,
        BaggingClassifier,KNeighborsClassifier,GaussianNB,SVC,GradientBoostingClassifier]

for i in models:
    model_selction_1(i)

summary_1=pd.DataFrame(model_summary_1).sort_values('f1_score_test',ascending=False).drop('model_name_test',axis=1)

summary_1

plt.figure(figsize=(7,6))
sns.barplot(y=summary_1['model_name_train'],x=summary_1['f1_score_test'])
plt.xticks(rotation=90)
plt.show()

"""##model selection for task 1

*  from the above graph it is found that the `bagging_classifier`,`gradiant boosting` performing well compared to other algorithms
* and it is performing well above 95 percentage so not using `optimization techniques` separatly

* im considering the `gradiant boosting` model over `bagging_classifier` as it performing better in more number of times compared to baggining classifer

* will create the `gradiant boosting` model for further use
"""

#model creation
#model initialization
high_priority_model=GradientBoostingClassifier()

#fitting the model
high_priority_model.fit(X_train,y_train)

#predicting using the model
high_priority_pred=high_priority_model.predict(X_test)

#printing the confusion metrics and classification report
print('metrics on test data')
print('confusion matrix')
print(confusion_matrix(y_test,high_priority_pred))
print('\n')
print('classification report')
print(classification_report(y_test,high_priority_pred))
print('==='*10)

# Save the model
with open('high_priority_model.pkl', 'wb') as file:
    pickle.dump(high_priority_model, file)

"""#TASK-2 | FORECASTING
**2. Forecast the incident volume in different fields , quarterly and
annual. So that they can be better prepared with resources and
technology planning.**
"""

data_1=df.copy()

data_1.head()

data_1.info()

"""

---
*  **sorting the data based on the ticket opening time**


---



---


"""

timeseries_data=data_1.sort_values('Open_Time')

timeseries_data.head()

"""---
*  as each time a single ticket raised from each department
* taking only CI_Cat column along with open_time
* will also consider only date neglecting the time in the timestamp
---
"""

forecast_data=timeseries_data[['CI_Cat','Open_Time']]

forecast_data['Open_Time']=forecast_data['Open_Time'].dt.date

forecast_data.head()

"""---
* **grouping is doing through the concept of pivot_table**
---
"""

pivot_table = forecast_data.pivot_table(index='Open_Time', columns='CI_Cat', aggfunc='size')

pd.set_option('display.max_rows',None)

pivot_table

"""---
*  converting the pivot table to dataframe
---
"""

final_df=pd.DataFrame(pivot_table)

"""---
* converting the index format from object type to datetime format
---
"""

final_df.index=pd.to_datetime(final_df.index)

"""---
* filling the null values with 0
---
"""

final_df.fillna(0,inplace=True)

len(final_df)

"""---
* resampling the data on day
* converting the daily data to quaterly year data
---
"""

daily_data = final_df.resample('D', closed='right', label='right').asfreq()

quaterly_data = daily_data.resample('Q').sum()

quaterly_data

quaterly_data.shape

plt.figure(figsize=(20,12))
pl_no=1
for i in quaterly_data.columns:
  plt.subplot(4,3,pl_no)
  quaterly_data[i].plot()
  plt.xlabel(i)
  plt.xticks(rotation=45)
  pl_no+=1
plt.tight_layout()

"""---
* all the columns are having the little sudden trend at some time
* and there is no seasonality found the data
* tried eliminating the trend with exponetial smootheing method but its resulting in very bad forecasting
---

#Arima model

##arima model forecasts and forecast plots
"""

#  Perform the forecasting for each column
arima_forecast = pd.DataFrame()
steps = 12
for column in quaterly_data.columns:
    model = ARIMA(quaterly_data[column], order=(1, 0, 0))  # ARIMA(1, 0, 0) model
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=steps)
    arima_forecast[column] = forecast

arima_forecast=arima_forecast.astype(int)

arima_forecast

plt.figure(figsize=(20,12))
pl_no=1
for i in arima_forecast.columns:
  plt.subplot(4,3,pl_no)
  arima_forecast[i].plot()
  plt.xlabel(i)
  plt.xticks(rotation=45)
  pl_no+=1
plt.tight_layout()

"""#Sarimax model"""

columns_to_forecast = quaterly_data.columns

# Perform the forecasting for each column
sarima_forecast = pd.DataFrame(columns=columns_to_forecast)
for column in columns_to_forecast:
    model = SARIMAX(quaterly_data[column], order=(1, 0, 0), seasonal_order=(1, 0, 0, 12))  # SARIMAX(1, 0, 0)(1, 0, 0, 12) model
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=12)  # Forecast for the next 12 months
    sarima_forecast[column] = forecast

sarima_forecast=sarima_forecast.astype(int)

sarima_forecast

"""##about forecast models
*  created 2 forecasting models for predicting the volumns quaterly and annualy
*  out of `arima_model` and `sarima_model` ,arima model performingvery well in forecasting and i plotted the results above.

#TASK 3
3. Auto tag the tickets with right priorities and right departments so that reassigning and related delay can be reduced
"""

data_3=df.copy()

data_3.head()

data_3=data_3.drop(['Open_Time','Resolved_Time','Close_Time'],axis=1)

X3=data_3.drop(['Priority','CI_Cat','Urgency'],axis=1)

X3.head()

y3=data_3['Priority']

y3.head()

y3_2=data_3['CI_Cat']

"""#Function for model selection Task 3


---
##Logic behind the function


---


 1. first creating a dictionary with the name model_summary and initiating with null values with proper keys

 2. function called `model_selection` will take model as parameter
 3.initially the model will be `initiated` within the function and will be `stored in the variable called model`
 4. model will be `fitted on x_train and y_train`
 5.model will `first predict on test data`
 6.after prediction all the evaluation  `metric values will be appended to dictionary` with corresponding key values.
 7.then it will `print the confusion matrix and classification report` of that model
 8.the same `steps will also the performed` on train data
 ---

"""

model_summary_2={'model_name_train':[],'f1_score_train':[],'recall_score_train':[],'accuracy_score_train':[],
               'model_name_test':[],'f1_score_test':[],'recall_score_test':[],'accuracy_score_test':[]}


def model_selction_2(model):

    #model initialization ,fitting and predicting
    print(model)
    model=model()
    model.fit(X_train,y_train)
    model_pred=model.predict(X_test)

    #appending the metrics to the dictionary created
    model_summary_2['model_name_test'].append(model.__class__.__name__)
    model_summary_2['f1_score_test'].append(f1_score(y_test,model_pred,average='macro'))
    model_summary_2['recall_score_test'].append(recall_score(y_test,model_pred,average='macro'))
    model_summary_2['accuracy_score_test'].append(accuracy_score(y_test,model_pred))

    #printing the confusion metrics and classification report
    print('metrics on test data')
    print(confusion_matrix(y_test,model_pred))
    print('\n')
    print(classification_report(y_test,model_pred))

    #predictions on train data
    model_pred1=model.predict(X_train)

    #appending the metrics to the dictionary created
    model_summary_2['model_name_train'].append(model.__class__.__name__)
    model_summary_2['f1_score_train'].append(f1_score(y_train,model_pred1,average='macro'))
    model_summary_2['recall_score_train'].append(recall_score(y_train,model_pred1,average='macro'))
    model_summary_2['accuracy_score_train'].append(accuracy_score(y_train,model_pred1))

    #printing the confusion metrics and classification report
    print('metrics on train data')
    print(confusion_matrix(y_train,model_pred1))
    print('\n')
    print(classification_report(y_train,model_pred1))
    print('==='*10)

X_train, X_test, y_train, y_test = train_test_split(X3, y3, test_size=0.3, random_state=42,stratify=y3)

for i in models:
    model_selction_2(i)

summary_2=pd.DataFrame(model_summary_2).sort_values('f1_score_test',ascending=False).drop('model_name_test',axis=1)

summary_2

plt.figure(figsize=(7,6))
sns.barplot(y=summary_2['model_name_train'],x=summary_2['f1_score_test'])
plt.xticks(rotation=90)
plt.show()

#model creation
#model initialization
all_priority_model=GradientBoostingClassifier()

#fitting the model
all_priority_model.fit(X_train,y_train)

#predicting using the model
all_priority_pred=all_priority_model.predict(X_test)

#printing the confusion metrics and classification report
print('metrics on test data')
print('confusion matrix')
print(confusion_matrix(y_test,all_priority_pred))
print('\n')
print('classification report')
print(classification_report(y_test,all_priority_pred))
print('==='*10)

# Save the model
with open('all_priority_model.pkl', 'wb') as file:
    pickle.dump(all_priority_model, file)

"""##Logic behind the function


---


 1. first creating a dictionary with the name model_summary and initiating with null values with proper keys

 2. function called `model_selection` will take model as parameter
 3.initially the model will be `initiated` within the function and will be `stored in the variable called model`
 4. model will be `fitted on x_train and y_train`
 5.model will `first predict on test data`
 6.after prediction all the evaluation  `metric values will be appended to dictionary` with corresponding key values.
 7.then it will `print the confusion matrix and classification report` of that model
 8.the same `steps will also the performed` on train data
 ---
"""

model_summary_3={'model_name_train':[],'f1_score_train':[],'recall_score_train':[],'accuracy_score_train':[],
               'model_name_test':[],'f1_score_test':[],'recall_score_test':[],'accuracy_score_test':[]}


def model_selction_3(model):

    #model initialization ,fitting and predicting
    print(model)
    model=model()
    model.fit(X_train,y_train)
    model_pred=model.predict(X_test)

    #appending the metrics to the dictionary created
    model_summary_3['model_name_test'].append(model.__class__.__name__)
    model_summary_3['f1_score_test'].append(f1_score(y_test,model_pred,average='macro'))
    model_summary_3['recall_score_test'].append(recall_score(y_test,model_pred,average='macro'))
    model_summary_3['accuracy_score_test'].append(accuracy_score(y_test,model_pred))

    #printing the confusion metrics and classification report
    print('metrics on test data')
    print(confusion_matrix(y_test,model_pred))
    print('\n')
    print(classification_report(y_test,model_pred))

    #predictions on train data
    model_pred1=model.predict(X_train)

    #appending the metrics to the dictionary created
    model_summary_3['model_name_train'].append(model.__class__.__name__)
    model_summary_3['f1_score_train'].append(f1_score(y_train,model_pred1,average='macro'))
    model_summary_3['recall_score_train'].append(recall_score(y_train,model_pred1,average='macro'))
    model_summary_3['accuracy_score_train'].append(accuracy_score(y_train,model_pred1))

    #printing the confusion metrics and classification report
    print('metrics on train data')
    print(confusion_matrix(y_train,model_pred1))
    print('\n')
    print(classification_report(y_train,model_pred1))
    print('==='*10)

X_train, X_test, y_train, y_test = train_test_split(X3, y3_2, test_size=0.3, random_state=42,stratify=y3_2)

for i in models:
    model_selction_3(i)

summary_3=pd.DataFrame(model_summary_3).sort_values('f1_score_test',ascending=False).drop('model_name_test',axis=1)

summary_3

plt.figure(figsize=(7,6))
sns.barplot(y=summary_3['model_name_train'],x=summary_3['f1_score_test'])
plt.xticks(rotation=90)
plt.show()

#model creation
#model initialization
department_classification_model=RandomForestClassifier()

#fitting the model
department_classification_model.fit(X_train,y_train)

#predicting using the model
department_classification_pred=department_classification_model.predict(X_test)

#printing the confusion metrics and classification report
print('metrics on test data')
print('confusion matrix')
print(confusion_matrix(y_test,department_classification_pred))
print('\n')
print('classification report')
print(classification_report(y_test,department_classification_pred))
print('==='*10)

# Save the model
with open('department_classification_model.pkl', 'wb') as file:
    pickle.dump(department_classification_model, file)

"""#Task 4
---
#Predict RFC (Request for change) and possible failure / misconfiguration of ITSM assets.
"""

data_4=df.copy()

data_4.head()

data_4['Category'].value_counts()

data_4.loc[data_4['Category']==2]

data_4.drop(data_4.loc[data_4['Category']==2].index,inplace=True)

X_4=data_4.drop(['Category','Open_Time','Resolved_Time','Close_Time'],axis=1)
y_4=data_4['Category']

"""##Logic behind the function


---


 1. first creating a dictionary with the name model_summary and initiating with null values with proper keys

 2. function called `model_selection` will take model as parameter
 3.initially the model will be `initiated` within the function and will be `stored in the variable called model`
 4. model will be `fitted on x_train and y_train`
 5.model will `first predict on test data`
 6.after prediction all the evaluation  `metric values will be appended to dictionary` with corresponding key values.
 7.then it will `print the confusion matrix and classification report` of that model
 8.the same `steps will also the performed` on train data
 ---
"""

model_summary_4={'model_name_train':[],'f1_score_train':[],'recall_score_train':[],'accuracy_score_train':[],
               'model_name_test':[],'f1_score_test':[],'recall_score_test':[],'accuracy_score_test':[]}


def model_selction_4(model):

    #model initialization ,fitting and predicting
    print(model)
    model=model()
    model.fit(X_train,y_train)
    model_pred=model.predict(X_test)

    #appending the metrics to the dictionary created
    model_summary_4['model_name_test'].append(model.__class__.__name__)
    model_summary_4['f1_score_test'].append(f1_score(y_test,model_pred,average='macro'))
    model_summary_4['recall_score_test'].append(recall_score(y_test,model_pred,average='macro'))
    model_summary_4['accuracy_score_test'].append(accuracy_score(y_test,model_pred))

    #printing the confusion metrics and classification report
    print('metrics on test data')
    print(confusion_matrix(y_test,model_pred))
    print('\n')
    print(classification_report(y_test,model_pred))

    #predictions on train data
    model_pred1=model.predict(X_train)

    #appending the metrics to the dictionary created
    model_summary_4['model_name_train'].append(model.__class__.__name__)
    model_summary_4['f1_score_train'].append(f1_score(y_train,model_pred1,average='macro'))
    model_summary_4['recall_score_train'].append(recall_score(y_train,model_pred1,average='macro'))
    model_summary_4['accuracy_score_train'].append(accuracy_score(y_train,model_pred1))

    #printing the confusion metrics and classification report
    print('metrics on train data')
    print(confusion_matrix(y_train,model_pred1))
    print('\n')
    print(classification_report(y_train,model_pred1))
    print('==='*10)

X_train, X_test, y_train, y_test = train_test_split(X_4, y_4, test_size=0.3, random_state=42,stratify=y_4)

for i in models:
    model_selction_4(i)

summary_4=pd.DataFrame(model_summary_4).sort_values('f1_score_test',ascending=False).drop('model_name_test',axis=1)

summary_4

plt.figure(figsize=(7,6))
sns.barplot(y=summary_4['model_name_train'],x=summary_4['f1_score_test'])
plt.xticks(rotation=90)
plt.show()

#model creation
#model initialization
category_classification_model=BaggingClassifier()

#fitting the model
category_classification_model.fit(X_train,y_train)

#predicting using the model
category_classification_pred=category_classification_model.predict(X_test)

#printing the confusion metrics and classification report
print('metrics on test data')
print('confusion matrix')
print(confusion_matrix(y_test,category_classification_pred))
print('\n')
print('classification report')
print(classification_report(y_test,category_classification_pred))
print('==='*10)

# Save the model
with open('possible_failure.pkl', 'wb') as file:
    pickle.dump(category_classification_model, file)
