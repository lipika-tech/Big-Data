#!/usr/bin/env python
# coding: utf-8

# 1.	Business Context 
# A new coronavirus designated 2019-nCoV was first identified in Wuhan, the capital of China's Hubei province. People developed pneumonia without a clear cause and for which existing vaccines or treatments were not effective The virus has shown evidence of human-to-human transmission. Transmission rate (rate of infection) appeared to escalate in mid-January 2020. As of 30 January 2020, approximately 8,243 cases had been confirmed. As the number of these cases was increasing at alarming rate, the WHO department decided to analyze the COVID data to find out the frequent patterns present in the entire world.
# 2.	Business Problem Understanding
# Every country has been affected by the virus's spread, which has caused chaos. Therefore, governments from each nation and WHO have determined that raising people's awareness of the virus' spread would be a first step toward giving them the fortitude to fight pandemics that might arise due to the rise in macho activities. 
# Data on the death rate, the number of people affected by the disease were gathered in order to retain knowledge of COVID in each nation. For each person to have access to historical statistics, this data needs to be transformed into a form that is useful. Using the data available, trends in the illness distribution attributable to each nation can be discovered.
# Your team has been appointed to take a closer look at the records of COVID dataset and analyze the effects caused due to the pandemic. 
# 1)	Identifying the spread among the countries and comparing them.
# 2)	Trying to know the reasons for the vast spread among few countries and the consequences caused because of the same. 
# 3.	Data Understanding 
# For this analysis, the department is expecting your team to explore the usage of MongoDB for the storage and querying the COVID_19 data. The data is available in Kaggle. Click here for accessing the dataset.  
# Below are the datasets which can be used to solve the respective questions / queries which are sub datasets of the main dataset.
# Q1) Country, Q2) World, Q3) Day, Q4) Country Q5) Country, Q6) Country, Q7) Country, Q8) Day, Q9) Covid19, Q10) FullGrouped, Q11) Covid 9, Q12) FullGrouped.
# 
# 

# In[6]:


#Importing packages
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import preprocessing
from pymongo import MongoClient

import warnings
warnings.filterwarnings('ignore')


# In[27]:


#Reading the datasets: country_wise_latest
country_wise_latest=pd.read_csv("country_wise_latest.csv")

#Renaming the column names
country_wise_latest.rename(columns = {'Country/Region':'Country_Region'}, inplace = True)
country_wise_latest.rename(columns = {'New cases':'New_cases'}, inplace = True)
country_wise_latest.rename(columns = {'New deaths':'New_deaths'}, inplace = True)
country_wise_latest.rename(columns = {'New recovered':'New_recovered'}, inplace = True)
country_wise_latest.rename(columns = {'Deaths / 100 Cases':'Deaths_Per_100_Cases'}, inplace = True)
country_wise_latest.rename(columns = {'Recovered / 100 Cases':'Recovered_Per_100_Cases'}, inplace = True)
country_wise_latest.rename(columns = {'Deaths / 100 Recovered':'Deaths_Per_100_Recovered'}, inplace = True)
country_wise_latest.rename(columns = {'Confirmed last week':'Confirmed_last_week'}, inplace = True)
country_wise_latest.rename(columns = {'1 week change':'1_week_change'}, inplace = True)
country_wise_latest.rename(columns = {'1 week % increase':'1_week_Pct_increase'}, inplace = True)
country_wise_latest.rename(columns = {'WHO Region':'WHO_Region'}, inplace = True)

print("Count of records and features: ",country_wise_latest.shape)

#Data types of features
country_wise_latest.info()

country_wise_latest.head(5).style.background_gradient(cmap='GnBu')


# In[33]:


#Data Preprocessing: country_wise_latest
print("Count of Missing Values: ")
country_wise_latest.isnull().sum()


# In[34]:


#EDA: country_wise_latest
print("Data distibution of numerical features: ")
country_wise_latest.describe()


# In[ ]:


sns.pairplot(data=country_wise_latest)


# In[5]:


#Reading the datasets: covid_19_clean_complete
longlat=pd.read_csv("covid_19_clean_complete.csv")
#Renaming the column names
longlat.rename(columns = {'Country/Region':'Country_Region'}, inplace = True)
longlat = longlat[['Country_Region','Lat','Long']]
longlat.drop_duplicates(keep='first', inplace=True)

# Merge DataFrames by Column
country_wise_latest2=pd.merge(country_wise_latest,longlat, on='Country_Region', how='left')
country_wise_latest2.head(2)


# In[ ]:


#Types: open-street-map, stamen-terrain
import plotly.express as px
fig = px.density_mapbox(country_wise_latest2, lat='Lat', lon='Long', z='Deaths', radius=10,
                        center=dict(lat=0, lon=180), zoom=0,
                        mapbox_style="open-street-map")
fig.show()


# In[ ]:


fig, axes = plt.subplots(round(len(country_wise_latest.columns) / 3), 3, figsize=(20, 30))

for i, ax in enumerate(fig.axes):
    if i < len(country_wise_latest.columns):
        ax.set_xticklabels(ax.xaxis.get_majorticklabels(), rotation=45)
        sns.countplot(x=country_wise_latest.columns[i], alpha=0.7, data=country_wise_latest, ax=ax)

fig.tight_layout()


# In[7]:


#Reading the datasets: covid_19_clean_complete
covid_19_clean_complete=pd.read_csv("covid_19_clean_complete.csv")

#Renaming the column names
covid_19_clean_complete.rename(columns = {'Country/Region':'Country_Region'}, inplace = True)
covid_19_clean_complete.rename(columns = {'Province/State':'Province_State'}, inplace = True)
covid_19_clean_complete.rename(columns = {'WHO Region':'WHO_Region'}, inplace = True)

print("Count of records and features: ",covid_19_clean_complete.shape)

#Data types of features
covid_19_clean_complete.info()

covid_19_clean_complete.head(5).style.background_gradient(cmap='GnBu')


# In[ ]:


#Data Preprocessing: covid_19_clean_complete
print("Count of Missing Values: ")
covid_19_clean_complete.isnull().sum()


# In[ ]:


#EDA: covid_19_clean_complete
print("Data distibution of numerical features: ")
covid_19_clean_complete.describe()


# In[ ]:


sns.pairplot(data=covid_19_clean_complete)


# In[ ]:


fig, axes = plt.subplots(round(len(covid_19_clean_complete.columns) / 3), 2, figsize=(20, 30))

for i, ax in enumerate(fig.axes):
    if i < len(covid_19_clean_complete.columns):
        ax.set_xticklabels(ax.xaxis.get_majorticklabels(), rotation=45)
        sns.countplot(x=covid_19_clean_complete.columns[i], alpha=0.7, data=covid_19_clean_complete, ax=ax)

fig.tight_layout()


# In[8]:


#Reading the datasets: worldometer_data
worldometer_data=pd.read_csv("worldometer_data.csv")

#Renaming the column names
worldometer_data.rename(columns = {'Country/Region':'Country_Region'}, inplace = True)
worldometer_data.rename(columns = {'Serious,Critical':'Serious_Critical'}, inplace = True)
worldometer_data.rename(columns = {'WHO Region':'WHO_Region'}, inplace = True)
worldometer_data.rename(columns = {'Tot Cases/1M pop':'Tot_Cases_Per_1M_pop'}, inplace = True)
worldometer_data.rename(columns = {'Deaths/1M pop':'Deaths_Per_1M_pop'}, inplace = True)
worldometer_data.rename(columns = {'Tests/1M pop':'Tests_Per_1M_pop'}, inplace = True)

print("Count of records and features: ",worldometer_data.shape)

#Data types of features
worldometer_data.info()

worldometer_data.head(5).style.background_gradient(cmap='GnBu')


# In[ ]:


#Data Preprocessing: worldometer_data
print("Count of Missing Values: ")
worldometer_data.isnull().sum()


# In[ ]:


#EDA: worldometer_data
print("Data distibution of numerical features: ")
worldometer_data.describe()


# In[ ]:


sns.pairplot(data=worldometer_data)


# In[ ]:


fig, axes = plt.subplots(round(len(worldometer_data.columns) / 4), 4, figsize=(20, 30))

for i, ax in enumerate(fig.axes):
    if i < len(worldometer_data.columns):
        ax.set_xticklabels(ax.xaxis.get_majorticklabels(), rotation=45)
        sns.countplot(x=worldometer_data.columns[i], alpha=0.7, data=worldometer_data, ax=ax)

fig.tight_layout()


# In[20]:


#Reading the datasets: usa_county_wise
usa_county_wise=pd.read_csv("usa_county_wise.csv")

#Renaming the column names
usa_county_wise.rename(columns = {'Long_':'Long'}, inplace = True)


print("Count of records and features: ",usa_county_wise.shape)

#Data types of features
usa_county_wise.info()

usa_county_wise.head(5).style.background_gradient(cmap='GnBu')


# In[ ]:


#Data Preprocessing: usa_county_wise
print("Count of Missing Values: ")
usa_county_wise.isnull().sum()


# In[ ]:


#EDA: usa_county_wise
print("Data distibution of numerical features: ")
usa_county_wise.describe()


# In[ ]:


sns.pairplot(data=usa_county_wise)


# In[ ]:


fig, axes = plt.subplots(round(len(usa_county_wise.columns) / 4), 4, figsize=(20, 30))

for i, ax in enumerate(fig.axes):
    if i < len(usa_county_wise.columns):
        ax.set_xticklabels(ax.xaxis.get_majorticklabels(), rotation=45)
        sns.countplot(x=usa_county_wise.columns[i], alpha=0.7, data=usa_county_wise, ax=ax)

fig.tight_layout()


# In[9]:


#Reading the datasets: full_grouped
full_grouped=pd.read_csv("full_grouped.csv")

#Renaming the column names
full_grouped.rename(columns = {'Country/Region':'Country_Region'}, inplace = True)
full_grouped.rename(columns = {'WHO Region':'WHO_Region'}, inplace = True)
full_grouped.rename(columns = {'WHO Region':'WHO_Region'}, inplace = True)
full_grouped.rename(columns = {'New cases':'New_cases'}, inplace = True)
full_grouped.rename(columns = {'New deaths':'New_deaths'}, inplace = True)
full_grouped.rename(columns = {'New recovered':'New_recovered'}, inplace = True)

print("Count of records and features: ",full_grouped.shape)

#Data types of features
full_grouped.info()

full_grouped.head(5).style.background_gradient(cmap='GnBu')


# In[ ]:


#Data Preprocessing: full_grouped
print("Count of Missing Values: ")
full_grouped.isnull().sum()


# In[ ]:


#EDA: full_grouped
print("Data distibution of numerical features: ")
full_grouped.describe()


# In[ ]:


sns.pairplot(data=full_grouped)


# In[ ]:


fig, axes = plt.subplots(round(len(full_grouped.columns) / 4), 4, figsize=(20, 30))

for i, ax in enumerate(fig.axes):
    if i < len(full_grouped.columns):
        ax.set_xticklabels(ax.xaxis.get_majorticklabels(), rotation=45)
        sns.countplot(x=full_grouped.columns[i], alpha=0.7, data=full_grouped, ax=ax)

fig.tight_layout()


# In[10]:


#Reading the datasets: day_wise
day_wise=pd.read_csv("day_wise.csv")

#Renaming the column names

day_wise.rename(columns = {'New cases':'New_cases'}, inplace = True)
day_wise.rename(columns = {'New deaths':'New_deaths'}, inplace = True)
day_wise.rename(columns = {'New recovered':'New_recovered'}, inplace = True)
day_wise.rename(columns = {'Deaths / 100 Cases':'Deaths_Per_100_Cases'}, inplace = True)
day_wise.rename(columns = {'Recovered / 100 Cases':'Recovered_Per_100_Cases'}, inplace = True)
day_wise.rename(columns = {'Deaths / 100 Recovered':'Deaths_Per_100_Recovered'}, inplace = True)
day_wise.rename(columns = {'No. of countries':'No_of_countries'}, inplace = True)

print("Count of records and features: ",day_wise.shape)

#Data types of features
day_wise.info()

day_wise.head(5).style.background_gradient(cmap='GnBu')


# In[ ]:


#Data Preprocessing: day_wise
print("Count of Missing Values: ")
day_wise.isnull().sum()


# In[ ]:


#EDA: day_wise
print("Data distibution of numerical features: ")
day_wise.describe()


# In[ ]:


sns.pairplot(data=day_wise)


# In[ ]:


fig, axes = plt.subplots(round(len(day_wise.columns) / 4), 4, figsize=(20, 30))

for i, ax in enumerate(fig.axes):
    if i < len(day_wise.columns):
        ax.set_xticklabels(ax.xaxis.get_majorticklabels(), rotation=45)
        sns.countplot(x=day_wise.columns[i], alpha=0.7, data=day_wise, ax=ax)

fig.tight_layout()


# In[11]:


#Reading the datasets: covid_19_clean_complete
covid_19_clean_complete=pd.read_csv("covid_19_clean_complete.csv")

#Renaming the column names
covid_19_clean_complete.rename(columns = {'Province/State':'Province_State'}, inplace = True)
covid_19_clean_complete.rename(columns = {'Country/Region':'Country_Region'}, inplace = True)
covid_19_clean_complete.rename(columns = {'WHO Region':'WHO_Region'}, inplace = True)


print("Count of records and features: ",covid_19_clean_complete.shape)

#Data types of features
covid_19_clean_complete.info()

covid_19_clean_complete.head(5).style.background_gradient(cmap='GnBu')


# In[ ]:


#Data Preprocessing: covid_19_clean_complete
print("Count of Missing Values: ")
covid_19_clean_complete.isnull().sum()


# In[ ]:


#EDA: covid_19_clean_complete
print("Data distibution of numerical features: ")
covid_19_clean_complete.describe()


# In[ ]:


sns.pairplot(data=covid_19_clean_complete)


# In[ ]:


fig, axes = plt.subplots(round(len(covid_19_clean_complete.columns) / 4), 4, figsize=(20, 30))

for i, ax in enumerate(fig.axes):
    if i < len(covid_19_clean_complete.columns):
        ax.set_xticklabels(ax.xaxis.get_majorticklabels(), rotation=45)
        sns.countplot(x=covid_19_clean_complete.columns[i], alpha=0.7, data=covid_19_clean_complete, ax=ax)

fig.tight_layout()


# In[ ]:


full_grouped
day_wise
covid_19_clean_complete
usa_county_wise
worldometer_data
country_wise_latest


# In[28]:


#Connecting with MongoDB
from pymongo import MongoClient

def run_query():
    client = MongoClient("mongodb://127.0.0.1:27017/")
    db = client['bigdata']
    return db


# In[29]:


#Insert logic should be run only once. 
#Code for deleting duplicates
#db["full_grouped"].delete_many({})


# In[30]:


#Dataset 1: country_wise_latest
dat1 = country_wise_latest
db = run_query()
db["country_wise_latest"].insert_many(dat1.to_dict('records'))


# In[16]:


#Dataset 2: full_grouped
dat2 = full_grouped
db = run_query()
db["full_grouped"].insert_many(dat2.to_dict('records'))


# In[17]:


#Dataset 3: day_wise
dat3 = day_wise
db = run_query()
db["day_wise"].insert_many(dat3.to_dict('records'))


# In[18]:


#Dataset 4: covid_19_clean_complete
dat4 = covid_19_clean_complete
db = run_query()
db["covid_19_clean_complete"].insert_many(dat4.to_dict('records'))


# In[21]:


#Dataset 5: usa_county_wise
dat5 = usa_county_wise
db = run_query()
db["usa_county_wise"].insert_many(dat5.to_dict('records'))


# In[81]:


#Dataset 6: worldometer_data
dat6 = worldometer_data
db = run_query()
db["worldometer_data"].insert_many(dat6.to_dict('records'))


# 
# # 5.	Expected Outcomes 

# ## 1)	The number of new cases, new deaths and new recovered

# In[22]:


from bson.json_util import dumps
db = run_query()
answ1 = db['country_wise_latest'].aggregate([{"$group" : { "_id" : "New_cases", "New_Cases_Sum" : { "$sum": "$New_cases" }}}])
print("New cases: ",dumps(list(answ1)))


# In[23]:


db = run_query()
answ2 = db['country_wise_latest'].aggregate([{"$group" : { "_id" : "New_deaths", "New_Deaths_Sum" : { "$sum": "$New_deaths" }}}])
print("New deaths: ",dumps(list(answ2)))


# In[24]:


db = run_query()
answ3 = db['country_wise_latest'].aggregate([{"$group" : { "_id" : "New_recovered", "New_Recovered_Sum" : { "$sum": "$New_recovered" }}}])
print("New recovered: ",dumps(list(answ3)))


# ## 2)	The number of death cases in each country of continent Asia and also the corresponding WHO regions
# 

# In[10]:


db = run_query()
answ1 = db['worldometer_data'].find({'Continent':'Asia'},{'Country_Region': 1, 'Continent':1, 'TotalDeaths':1})
print("Sum of Deaths at country level: ")
pd.DataFrame(answ1)


# ## 3)	The number of deaths that occurred on 12-02-2020
# 

# In[11]:


db = run_query()
answ1 = db['day_wise'].find({'Date':"2020-02-12"},{'Date':1,'New_deaths': 1, 'Deaths': 1})
print("Sum of Deaths on 12th Dec 2020 only is 5: ")
print("Sum of Deaths till 12th Dec 2020 are 1118: ")
pd.DataFrame(answ1)


# ## 4)	The number of active new cases (new cases-(new death+new recovered)) in a reverse sorted order based on the country name

# In[12]:


db = run_query()
answ1 = db['country_wise_latest'].aggregate([{"$project":{ '_id':0, 'Country_Region': 1,'Active_New_Cases': { "$subtract":["$New_cases",{ "$add": ["$New_deaths", "$New_recovered" ]}]}}},{"$sort" : {'Country_Region': -1}}])
print("Number of active new cases with reverse country names: ")
pd.DataFrame(answ1)


# ## 5)	The names of the countries with more than 9000 active cases and more than 800 deaths

# In[13]:


db = run_query()
answ1 = db['country_wise_latest'].find({"Active" : {"$gt": 9000 },"Deaths" : {"$gt": 800 }}, {'Country_Region': 1,'Active': 1,'Deaths': 1,'_id': 0})
print("Names of the countries with more than 9000 active cases and more than 800 deaths: ")
pd.DataFrame(answ1)


# ## 6)	The country with the highest number of active cases and also with second highest death rate

# In[33]:


db = run_query()
ans1 = db["country_wise_latest"].find({},{
     '_id': 0,
 'Country_Region': 1,
 'Active': 1
 }).sort("Active", -1).limit(1)
print(" The country with the highest number of active cases: ")
pd.DataFrame(ans1)


# In[41]:


db = run_query()
ans1 = db["country_wise_latest"].find({},{
     '_id': 0,
 'Country_Region': 1,
 "Deaths_Per_100_Cases":1
 }).sort("Deaths_Per_100_Cases", -1).skip(1).limit(1)
print(" The country with second highest death rate: ")
pd.DataFrame(ans1)


# ## 7)	The total number of deaths all around the world

# In[17]:


db = run_query()
answ1 = db['country_wise_latest'].aggregate([
{ "$group": {
 "_id":1,
 "totalDeaths": {
 "$sum": "$Deaths"
 }
}}
]);

print("Total number of deaths all around the world: ")
pd.DataFrame(answ1)


# ## 8)	The number of death cases and active cases between 28-01-2020 and 21-02-2020

# In[18]:


db = run_query()
answ1 = db['day_wise'].aggregate([
{"$match" : {"Date": { "$gte": "2020-01-28"}}},
{"$match" : {"Date": { "$lte": "2020-02-21"}}},
{"$group" :{"_id": 0, "TotalDeaths_From_28012020_To_21022020": {"$sum": "$Deaths"}, "TotalActive_From_28012020_To_21022020": {"$sum": "$Active"}}},
{"$project": {"_id":0, "TotalDeaths_From_28012020_To_21022020":1, "TotalActive_From_28012020_To_21022020":1}}])
print("Number of death cases and active cases between 28-01-2020 and 21-02-2020: ")
pd.DataFrame(answ1)


# ## 9)	The latitude and longitude of countries ending with “ia” and the number of countries

# In[19]:


db = run_query()
answ1 = db['covid_19_clean_complete'].find({'Country_Region': {'$regex':'ia$'}},{'Country_Region':1,'Lat':1,'Long':1})
answ2 = db['covid_19_clean_complete'].find({'Country_Region': {'$regex':'ia$'}},{'Country_Region':1,'Lat':1,'Long':1})
print("The latitude and longitude of countries ending with 'ia': ")
print("Number countries ending with “ia”: ",len((pd.DataFrame(answ1)['Country_Region']).unique()))
pd.DataFrame(answ2)


# ## 10)	The countries with active cases on 30/03/2020

# In[20]:


db = run_query()
answ1 = db['full_grouped'].find({"Date" : {"$eq": "2020-03-30"}, "Active": { "$gte": 1 }},{'Date':1,'Active': 1 , "Country_Region": 1})
answ2 = db['full_grouped'].find({"Date" : {"$eq": "2020-03-30"}, "Active": { "$gte": 1 }},{'Date':1,'Active': 1 , "Country_Region": 1})
print("Number countries with active cases on 30/03/2020: ",len((pd.DataFrame(answ1)['Country_Region']).unique()))
print("The countries with active cases on 30/03/2020: ")
pd.DataFrame(answ2)


# ## 11)	The latitude and longitude of those countries which are having active cases greater than 100

# In[21]:


db = run_query()
answ1 = db['covid_19_clean_complete'].find({'Active': {'$gt': 100}},{"Country_Region":1,'Lat':1,'Long':1,'Active':1})
answ2 = db['covid_19_clean_complete'].find({'Active': {'$gt': 100}},{"Country_Region":1,'Lat':1,'Long':1,'Active':1})
print("Number countries with active cases greater than 100: ",len((pd.DataFrame(answ1)['Country_Region']).unique()))
print("The countries with active cases on 30/03/2020: ")
pd.DataFrame(answ2)


# ## 12)	The countries and respective dates in which maximum increase of active cases occurred.

# In[22]:


db = run_query()
ans1 = db['full_grouped'].aggregate([
    {
       
        "$project": {"Date": 1,
                                   "Country_Region": 1,
                                   "Active" :1,
                                   "New_cases":1,
                                   "New_deaths":1,
                                   "New_recovered":1,
                                   "Difference": {"$subtract":["$New_cases",{"$add": ["$New_deaths", "$New_recovered"]}]
                                  }} 
        
    },
 {
    "$group": {
      "_id": "$Country_Region",
      "max_diffrence": {
        "$max": "$Difference"
      },
      "records": {
        "$push": "$$ROOT"
      }
    }
  },
    {
    "$project": {
      "items": {
        "$filter": {
          "input": "$records",
          "as": "records",
          "cond": {
            "$eq": [
              "$$records.Difference",
              "$max_diffrence"
            ]
          }
        }
      }
    }
  },
  {
    "$unwind": "$items"
  },
  {
    "$replaceWith": "$items"
  }
    

])

pd.DataFrame(ans1)


# In[ ]:





# In[ ]:




