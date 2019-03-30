#!/usr/bin/env python
# coding: utf-8

# # IST 652 Lab #5
# ### Instructions
# - Complete all 6 questions in this assignment.
# - You may work with others, <b> but the work you submit must be your own </b>. You can differentiate your work by adding comments or changing the values you use to test your code. However, submitting some else's work as your own is an academic integrity violation and will be raised to academic affairs.
# - It is always better to attempt a problem as partial credit may be granted.
# 
# 
# ### Submission Guide:
# - Submit your answers on BlackBoard by Saturday 2019-03-30.
# - The file must be either a .py or .ipynb file type.
# - <i><span style="color:red">The name of the file you submit should be <i><b> ist652_lab5_lastname.py (.ipynb) </i></b>.</span>
# 
# 
# 
# ### Grading [ 6 total points ]
# For Each Questions (1-6), the following credit will be awarded:
# - 0.75 for printing the correct answer to the console.
# - 0.15 for approaching the problem efficiently.
# - 0.05 for properly documenting and commenting your code.
# 

# ---
# ## Questions

# ### Analysis of Given Names @ Data.Gov
# - https://catalog.data.gov/dataset/most-popular-baby-names-by-sex-and-mothers-ethnic-group-new-york-city-8c742
# ![image.png](attachment:image.png)

# ---

# #### ( 1a ) Fetch the online data from the following location and convert it into a python JSON object:
# - https://data.cityofnewyork.us/api/views/25th-nujf/rows.json?accessType=DOWNLOAD
# - please use the packages below which we covered in class (urllib and json)
# 
# ####  (1b) Create a new list variable called "name_data" which are the values associated with the JSON key = 'data'.
# 
# 
# ##### [1 point]

# In[308]:


import urllib
import json


# In[322]:


# Enter your code here, printing relevant answers to console:
#1a:
data_url = "https://data.cityofnewyork.us/api/views/25th-nujf/rows.json?accessType=DOWNLOAD"
response = urllib.request.urlopen(data_url)
type(response)


# In[323]:


#1b:
json_string = response.read().decode('utf-8') #decode bytestring to utf-8
#print(json_string[:1000])

#use the json package to transform the string to Python data structures consisting of lists and dictionaries
eq_parsed_json = json.loads(json_string) 
print(type(eq_parsed_json))

eq_parsed_json.keys()

name_data = eq_parsed_json['data']
print(name_data[0])


# In[324]:


print(json.dumps(name_data[0], indent=2))


# ---
# #### ( 2a ): Create a dataframe from the values in "name_data" list
# - For each name in the "name_data" list, the only data we care about are the following indices:
#     - name[8] which is the year
#     - name[9] which is the gender
#     - name[10] which is the ethnicity
#     - name[11] which is the name
#     - name[12] which is the instance of the name
#     - name[13] which is the rank of the name within the year/gender/enthnicity group
# - Additionally, be sure that series which are numbers are cast as float or np.float datatypes.
# 
# #### ( 2b ): Display the summary statistics of <u>both</u> the numeric and string data in the dataframe using the describe method.
# 
# ##### [1 point]

# In[325]:


# Enter your code here, printing relevant answers to console:
import pandas as pd
from pandas.io.json import json_normalize

#2a:
namelist = []
for name in name_data:
    namelist.append({'year': float(name[8]),
                   'gender': name[9],
                   'ethnicity': name[10],
                   'name': name[11],
                   'instance': float(name[12]),
                   'rank': float(name[13])})
    
nameDF = pd.DataFrame(namelist)
print(nameDF)
type(nameDF)


# In[113]:


#2b:
nameDF.describe() #for numeric variables


# In[127]:


import numpy as np
nameDF.describe(exclude=[np.number]) #for non-numeric columns


#  ----

# #### ( 3a ):  Create a new dataframe by aggregating the dataframe from (2a) to the following level:
# - Group by Gender, Name and return the sum of name instances (name[12] from 2a)
# 
# #### ( 3b ): Count the number of distinct names in the dataframe created in (3a).
# - If Alex is a FEMALE and a MALE name, still only count this name once.
# 
# #### ( 3c ): Create a list of distinct names which are assigned to both FEMALE and MALE children and print the length of the list.
# 
# 
# ##### [1 point]

# In[419]:


# Enter your code here, printing relevant answers to console:
#3a:
grouped = nameDF.groupby(['gender', 'name']).agg({'instance':[sum]})
grouped


# In[351]:


#3b:
grouped1 = nameDF.groupby(['name']).agg({'instance':[sum]})
grouped1


# In[418]:


#3c:
#Create a list of distinct names which are assigned to both FEMALE and MALE children and print the length of the list.¶

#create a df grouped by name and gender, then count number of times names appeared per gender.
grouped3 = nameDF.groupby(['name', 'gender'])['name'].count().unstack('gender')

#only keep the rows (names) that have non-null values for both males and females.
filtered = grouped3[grouped3['FEMALE'].notnull() & grouped3['MALE'].notnull()]
filtered
#print("Number of unisex names:", len(filtered))


# ----

# #### ( 4 ) Create a new pivoted dataframe ( e.g. use pd.pivot() ) from (2a) such that:
# - We are only considering:
#     - year = '2013'
#     - gender = 'FEMALE'
#     - rank <= 10
# - The pd.pivot() method maps the following parameters:
#     - index = 'ethnicity'
#     - columns = 'rank'
#     - values = 'name'
# 
# The resulting dataframe should look like:
# ![image.png](attachment:image.png)
# 
# ##### [1 point]

# In[426]:


# Enter your code here, printing relevant answers to console:
pivotDF = nameDF[(nameDF['year'] == 2013) & (nameDF['gender'] == 'FEMALE') & (nameDF['rank'] <= 10)]

pivotDF.pivot(index = 'ethnicity', columns = 'rank', values = 'name')






# ---

# ### MongoDB

# ---
# #### ( 5a ): Convert the dataframe from (2b) to a list of dictionaries.
# - It's highly recommended that you use the method <i>pd.to_dict(orient='records')</i>
# 
# #### ( 5b ): Create a MongoDB database called 'names_db'
# - IMPORTANT: Don't forget to make sure the MongoDB session is active
#     - run ```$ mongod``` in the terminal
# - Use pymongo package for operating on MongoDB databases
# 
# #### ( 5c ): Load the list of dictionaries from (5a) into a collection called "names" in the database "names_db" from (5b)
# 
# 
# ##### [1 point]

# In[209]:


# Enter your code here, printing relevant answers to console:
from pymongo import MongoClient
client = MongoClient('localhost', 27017)


# In[435]:


#5a:
convert = nameDF.to_dict(orient='records')
convert[:1]


# In[245]:


#5b:
mydb = client.names_db #create databse called names_db

#check if the database exists
dblist = client.list_database_names()
if "names_db" in dblist:
  print("The database exists.")


# In[246]:


#5c:
mycol = mydb['names'] #create collection called 'names'
type(mycol) #type: pymongo.collection.Collection

#check if collection(table) exists
collist = mydb.list_collection_names()
if "names" in collist:
  print("The collection exists.")

x = mycol.insert_many(convert) #load the list of dictionaries frm 5a into the 'names' database


# In[298]:


#fetch all five docs just to check if the codes ran properly
docs = mycol.find()
for doc in docs[:5]:
    print(doc)


# ---
# #### ( 6a ): Return the following records from the MongoDB collection "names" you created in (5b)
# - All records which are of rank >= 100
# - All records where the name == 'Grace'
# - All records where the gender == 'MALE' AND where the year = '2016'
#     - Also, return the records sorted by gender 
# 
# #### ( 6b ): Count the number of records in the Mongo Collection "names" where:
# - The name "Sarah" is in the top 5 (i.e. rank <= 5)
# - The rank >= 15 and the year is 2012
# - The count of name instances is greater than 350
# 
# ##### [1 point]

# In[441]:


# Enter your code here, printing relevant answers to console:
#6a:

#rank over 100
results1 = mycol.find({'rank': {'$gte':100}})
#for result in results1:
    #print(result)

#name == 'Grace'
results2 = mycol.find({'name': 'Grace'})
#for result in results2:
    #print(result)

#gender == MALE AND year == 2016
results3 = mycol.find({"$and": 
                       [{'gender':'MALE'},
                       {'year':{'$eq':2016}}]
                     })
#for result in results3:
    #print(result)


# In[442]:


#6b:
#Sarah with top 5 rank
results4 = mycol.count_documents({'$and':
                                  [{'name':'Sarah'},
                                  {'rank':{'$lte':5}}]})
print(results4)

#>=15 rank in year 2012
results5 = mycol.count_documents({'$and':
                                  [{'year':{'$eq':2012}},
                                  {'rank':{'$gte':15}}]})
print(results5)

#instances > 350
results6 = mycol.count_documents({'instance':{'$gt':350}})
print(results6)

