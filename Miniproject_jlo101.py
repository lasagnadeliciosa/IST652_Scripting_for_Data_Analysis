#!/usr/bin/env python
# coding: utf-8

# In[60]:


import pandas as pd #to read csv
import numpy as np
import re #regex


# In[176]:


import csv
#the dataset
pokemon = '/Users/jenyeulo/Documents/Syracuse_University/IST652/MiniProject/pokemonDataset2.csv'


# In[177]:


#read csv into dataframe
pokeDF = pd.read_csv(pokemon)


# In[178]:


#data cleaning:
#dropping unwanted columns:
to_drop = ['against_bug',
           'against_dark',
           'against_dragon',
           'against_electric',
           'against_fairy',
           'against_fight',
           'against_fire',
           'against_flying',
           'against_ghost',
           'against_grass',
           'against_ground',
           'against_ice',
           'against_normal',
           'against_poison',
           'against_psychic',
           'against_rock',
           'against_steel',
           'against_water',
           'abilities',
           'percentage_male',]
pokeDF.drop(columns=to_drop, inplace = True)


# In[81]:


pokeDF.head() #reinspect the dataframe to make sure the columns are right.


# In[82]:


#drop the NA values
pokeDF.dropna()


# In[83]:


pokeDF.iloc[0] #inspect the first row of the dataframe


# In[179]:


#Question 1: legendary vs. non legendary difficulty of capture by generation
#rename a column
pokeDF = pokeDF.rename(columns={'is_legendary': 'legendary'})
print(type('legendary'))


# In[180]:


#data analysis:
#divide the legendary pokemons from those that are not:
pokeN = pokeDF.loc[pokeDF['legendary'] == False]
pokeY = pokeDF.loc[pokeDF['legendary'] == True]


# In[181]:


#count the numbers and calculate the proportions of legendary pokemons vs. non-legendary
countL = [pokeN['name'].count(), pokeY['name'].count()]
propL = pokeY['name'].count() / pokeN['name'].count()
print(countL, propL)


# In[248]:


#we will create a for loop to store the average capture rate of legendary vs. non-legendary in each generation.
data = [] #create an empty list so that we can convert it to a dataframe later.
for i in range(1,8):
    datarow = [i] #append generation number into a list and await for further process

    genrationDF = pokeDF.loc[pokeDF['generation'] == i] #filter by generation == i
    legendDF = genrationDF.loc[pokeDF['legendary'] == True] #pulls legendary pokemon in generationDF
    datarow.append(legendDF['capture_rate'].astype(np.int64).mean()) #convert capture_rate to int because it's orginally a string
    nonLegendDF = genrationDF.loc[pokeDF['legendary'] == False] #pulls non-legendary pokemon in generationDF
    datarow.append(nonLegendDF['capture_rate'].astype(np.int64).mean())
    data.append(datarow) #append our list into the data variable creating a list of list structure, awaiting to be converted to a dataframe
    
print(data)


# In[249]:


#finally create a dataframe and output the summary into csv file.

newPokeDF = pd.DataFrame(data, columns=['Generation', 'Legendary', 'Not Legendary']) #create dataframe with headings.
print(newPokeDF)


# In[217]:


#export result as csv
newPokeDF.to_csv('legend-nonlegend_capture_mean.csv')


# In[ ]:


#combined stat (attack+defense+hp+speed) by types


# In[245]:


#Question 2: Combined stat (attach+defense+hp+speed) analysis by types.
types = pokeDF['type1'].unique() #type 1 and 2 has equal values, except type2 could contain 'nan' for null values, as not all pokemons has two types.

pokeDF['overall'] = pokeDF['attack'] + pokeDF['defense'] + pokeDF['hp'] + pokeDF['speed'] / 4 #create a new column called "overall" which is the average of four attributes.

data = []
for pokeType in types:
    #inspect dataframe two times, first time as 'type1' == pokeType, then second time as 'type2' == pokeType.
    type1Poke = pokeDF.loc[pokeDF['type1'] == pokeType]
    type2Poke = pokeDF.loc[pokeDF['type2'] == pokeType] # does not contain pokemon with no type2 attributes
    
    combinedDF = pd.concat([type1Poke, type2Poke]) #merge two new dataframe into one.
    
    #find out the values for each type
    data.append([ 
        pokeType, 
        combinedDF['overall'].max(),
        combinedDF['overall'].min(),
        combinedDF['overall'].mean(),
        combinedDF['overall'].median(),
        combinedDF['overall'].std(),
        combinedDF['overall'].count(),
    ])
    
print(data)

#create a new dataframe with headings
newPokeDF = pd.DataFrame(data, columns=['Type',
                                        'Max Value', 
                                        'Min Value', 
                                        'Mean',
                                        'Median',
                                        'Standard Deviation',
                                        '# of Pokemons'])
print(newPokeDF)


# In[247]:


#export result as csv
newPokeDF.to_csv('overallScoreByType.csv')

