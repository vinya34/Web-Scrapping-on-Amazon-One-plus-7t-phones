#!/usr/bin/env python
# coding: utf-8

# In[8]:


get_ipython().system('pip install beautifulsoup4')


# In[9]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
import re
import time
from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests


# In[10]:


no_pages = 100

def get_data(pageNo):  
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

    r = requests.get('https://www.amazon.in/Test-Exclusive-748/product-reviews/B07DJLVJ5M/ref=cm_cr_arp_d_paging_btm_next_2'+str(pageNo)+'?ie=UTF8&reviewerType=all_reviews&pageNumber='+str(pageNo), headers=headers)
    content = r.content
    soup = BeautifulSoup(content)
    #print(soup)

    alls = []
    for d in soup.findAll('div', attrs={'class':'a-section review aok-relative'}):
        #print(d)
        
        
        
        name = d.find('span', attrs={'class':'a-profile-name'})
        date=d.find('span',attrs={'class':'a-size-base a-color-secondary review-date'})
        review=d.find('span',attrs={'class':'a-size-base review-text review-text-content'})
        helpful_to=d.find('span',attrs={'class':'a-size-base a-color-tertiary cr-vote-text'})
        title=d.find('a',attrs={'class':'a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold'})
        rating=d.find('span',attrs={'class':'a-icon-alt'})
       

        all1=[]

        if name is not None:
            
            all1.append(name.text)
        else:
            all1.append("unknown-product")

        if date is not None:
         
            all1.append(date.text)
        else:    
            all1.append('date not mentioned')

        if review is not None:
            
            all1.append(review.text)
        else:
            all1.append('no review')     

        if helpful_to is not None:
            
            all1.append(helpful_to .text)
        else:
            all1.append('0')
            
        if title is not None:
            
            all1.append(title.text)
        else:
            all1.append('no title')
            
        if rating is not None:
            
            all1.append(rating.text)
        else:
            all1.append('no rating')
            
        alls.append(all1)    
    return alls


# In[11]:


results = []
for i in range(1, no_pages+1):
    results.append(get_data(i))
flatten = lambda l: [item for sublist in l for item in sublist]
df = pd.DataFrame(flatten(results),columns=['Name','Date','Review','Helpful_to','Title','Rating'])
df.to_csv('amazon_reviewss.csv', index=False, encoding='utf-8')


# In[12]:


df = pd.read_csv("amazon_reviewss.csv")


# In[13]:


df.head(10)


# In[14]:


df.info()


# In[15]:


print(df)


# In[16]:


print(df['Review'])


# In[18]:


df['Rating'] = df['Rating'].apply(lambda x: x.split()[0])


# In[19]:


df['Rating'] = pd.to_numeric(df['Rating'])


# In[27]:


print(df['Rating'])


# In[21]:


df["Review"] = df["Review"].str.replace(',', '')


# In[22]:


df['Title']=df['Title'].str.replace(',', '')


# In[23]:


df["Review"] = df["Review"].str.replace('\n', '')


# In[26]:


df['Title']=df['Title'].str.replace('\n', '')


# In[28]:


df.head()


# In[29]:


df['Helpful_to'] = df['Helpful_to'].apply(lambda x: x.split()[0])


# In[31]:


print(df['Helpful_to'])


# In[32]:


df.head()


# In[33]:


df["Date"] = df["Date"].str.replace('Reviewed in India on', '')


# In[34]:


df.head()


# In[35]:


df.to_csv('amazon_reviews_final.csv', index=False, encoding='utf-8')


# In[ ]:




