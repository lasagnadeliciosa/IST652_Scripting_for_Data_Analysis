#!/usr/bin/env python
# coding: utf-8

# # IST 652 Lab #4
# ### Instructions
# - Complete all 6 questions in this assignment.
# - You may work with others, <b> but the work you submit must be your own </b>. You can differentiate your work by adding comments or changing the values you use to test your code. However, submitting some else's work as your own is an academic integrity violation and will be raised to academic affairs.
# - It is always better to attempt a problem as partial credit may be granted.
# 
# 
# ### Submission Guide:
# - Submit your answers on BlackBoard by Saturday 2019-03-23.
# - The file must be either a .py or .ipynb file type.
# - <i><span style="color:red">The name of the file you submit should be <i><b> ist652_lab4_lastname.py (.ipynb) </i></b>.</span>
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

# ### Web Scraping: HTML

# #### ( 1a ) Choose a web site and retrieve the HTML data using urllib.
# - If it doesn’t return a page (perhaps because it uses cookies or other interactions to actually return content), try a different site.
#     - <b>NOTE:</b> Some sites (e.g. Google) blocks webscrapers so your code will run once or twice, but then fail. Please be conscious of this.
#     
# #### ( 1b ) Use BeautifulSoup to parse the object (like we did in class).
# 
# <br><b>NOTE:</b> The BeatifulSoup object will be used in (2) and (3).
# 
# ##### [1 point]

# In[9]:


from urllib import request
from bs4 import BeautifulSoup


# In[2]:


# Enter your code here, printing relevant answers to console:
#1a
wgurl = "https://shop.tcgplayer.com/magic/product/show?ProductName=black%20lot&newSearch=false&ProductType=All"
response = request.urlopen(wgurl)
html = response.read().decode('utf8')
#print(html[:500])


# In[3]:


#1b
htmlsoup = BeautifulSoup(html,'html.parser') #parse with beautifulsoup
type(htmlsoup)


# ---
# #### ( 2 ): Count the number of hyperlink URLs (which begin with http) in the <u>head</u> & <u>body</u> tags.
# 
# ##### [1 point]

# In[54]:


# Enter your code here, printing relevant answers to console:
anchors = htmlsoup.find_all('a') #find all the <a... anchors
#print(anchors[:8])

#for each anchor <a.., we use the href attricute to get the actual anchor part
links = [str(link.get('href')) for link in anchors] 
#print(links[ :8])

urls = [link for link in links if link.startswith('http')]
#print(urls[:8])
print('Link counts:', len(urls))


#  ----

# #### ( 3a ):  Generate a unique list of hyperlink URLs (which begin with http) from the <u>body</u> tag and convert it into a pandas <u>series</u> object.
# - If your website body has no hyperlinks, please select a new website and repeat question (1).
# 
# 
# #### ( 3b ):  Create a function which parses the domain name (parent website) from a hyperlink URL.
# - for example:
#     - <b>URL:</b> http://www.espn.com/mens-college-basketball/story/_/id/26281956/know-every-team-bracket
#     - <b>domain name:</b> espn.com
#         - or www.espn.com
# 
# #### ( 3c ): Create a new pandas series composed of domain names.
# - Consider using the <b>series.map()</b> method, applying your function from (3b) over the series in (3a)
# 
# ##### [1 point]

# In[5]:


import pandas as pd


# In[59]:


# Enter your code here, printing relevant answers to console:
#3a
urlSeries = pd.Series(urls)
#print(urlSeries)

#3b
def domainParser(url): #this function is used to parse the domain name
    return url.split('/')[2] #keep the second index of the array after spliting.

#3c
domainSeries = urlSeries.map(domainParser).drop_duplicates() #apply function to all urls and then de-duplicate using .drop_duplicates.
print(domainSeries)


# ----

# ### Web Scraping: XML

# #### ( 4a ) Choose an RSS feed site and retrieve the XML data using urllib.
# - If it doesn’t return a page (perhaps because it uses cookies or other interactions to actually return content), try a different site.
# - Here is a list of RSS Feeds to get you started:
#     - <b>https://rss.com/popular-rss-feeds/</b>
# 
# #### ( 4b ) Use ElementTree to parse the object (like we did in class).
# 
# 
# ##### [1 point]

# In[12]:


# Enter your code here, printing relevant answers to console:
#4a
rss = 'https://feeds.a.dj.com/rss/RSSWSJD.xml'
techXML = request.urlopen(rss).read().decode('utf8')
#print(techXML[:500])


# In[13]:


#4b
import xml.etree.ElementTree as etree
import io
xmlfile = io.StringIO(techXML)
tree = etree.parse(xmlfile)
type(tree)


# ---
# #### ( 5 ): Count the number of Top-level <u>parent tags</u> & their number of <u>child</u> tags.
# - Top-level means that a tag has <b><u>no</b></u> parent tag
# - Only count direct children to these top level tags
#     - Do not count grandchildren, etc
# 
# ##### [1 point]

# In[61]:


# Enter your code here, printing relevant answers to console:
root = tree.getroot()
print('rss', len(root))

for child in root:
    print(child.tag, len(child))
    
channel = root[0] #get the first and only child from root, which is "channel"


# ---
# #### ( 6a ): Convert all of the items of your RSS XML into a pandas dataframe.
# - An item in an RSS feed begins with an item tag < item > ... < /item >
# - Each row represents 1 item
# - Each column represents 1 child-tag to the parent <u>item</u> tag:
#     - i.e.: Title, Link, PubDate, Category
#         - Ignore children of these tags
# 
# #### ( 6b ): Provide summary statistics about the dataframe.
# - Consider using the .describe() method
# 
# ##### [1 point]

# ### FOR EXAMPLE
# https://api.foxsports.com/v1/rss?partnerKey=zBaFxRyGKCfxBagJG9b8pqLyndmvo7UU&tag=soccer
# ![image.png](attachment:image.png)

# In[33]:


# Enter your code here, printing relevant answers to console:
#6a
itemlist = channel.findall('item')
len(itemlist)

#step 1 create header

headers = [itemspecs.tag for itemspecs in itemlist[0]]
#print(header)

#step 2 scrape out data from xml and create list of list

table = [[element.text for element in item] for item in itemlist]
#print(table)

df = pd.DataFrame(table, columns=headers)
print(df)


# In[39]:


#6b
df.groupby('{http://dowjones.net/rss/}articletype')['title'].nunique()

#df = df.groupby('domain')['ID'].nunique()

