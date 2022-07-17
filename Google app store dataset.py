#!/usr/bin/env python
# coding: utf-8

# # Google App Store Dataset (EDA)

# In[1]:


import pandas as pd
import numpy as np
import seaborn as sns
import json
import os


# In[1]:


#Importing data into notebook


# In[81]:


data = pd.read_csv(r"C:\Users\varun\OneDrive\Documents\Python\New Folder\Project testing\googleplaystore.csv")
user_review = pd.read_csv(r"C:\Users\varun\OneDrive\Documents\Python\New Folder\Project testing\googleplaystore_user_reviews.csv")


# In[3]:


data


# In[4]:


data.columns


# In[5]:


data.dtypes


# # Data Cleaning

# In[6]:


data["Category"].unique()


# In[7]:


data["Category"].value_counts()


# In[8]:


data[data['Category']=='1.9']


# In[9]:


data['App'].loc[10472]=data['Category'].loc[10472]
data['Category'].loc[10472] = np.nan
data.loc[10472]


# In[10]:


data["Category"].value_counts()


# In[11]:


data["Rating"].unique()


# In[12]:


data["Rating"].value_counts()


# In[13]:


data['rating'] = pd.to_numeric(data['Rating'], errors='coerce')
data['Rating'].dtype


# In[14]:


data["Reviews"].unique()


# In[15]:


data["Reviews"].nunique()


# In[16]:


data["Reviews"].value_counts()


# In[17]:


data['Reviews'] = data.Reviews.replace("3.0M",3000000.0)
data['Reviews'] = data['Reviews'].astype(float)
data['Reviews'].dtype


# In[18]:


data.head(2)


# In[19]:


data["Size"].unique()


# In[20]:


data['Size'] = data.Size.replace("Varies with device",np.nan)
data['Size'] = data.Size.str.replace("M","000")
data['Size'] = data.Size.str.replace("k","")
data['Size'] = data.Size.replace("1,000+","1000")
data['Size'] = data['Size'].astype(float)


# In[21]:


data['Size'].dtype


# In[22]:


data["Installs"].unique()


# In[23]:


data['Installs'] = data.Installs.str.replace(",","")
data['Installs'] = data.Installs.str.replace("+","")
data['Installs'] = data.Installs.replace("Free",np.nan)
data['Installs'] = data['Installs'].astype(float)


# In[24]:


data['Installs'].dtype


# In[25]:


data["Price"].unique()


# In[26]:


data['Price'] = data.Price.replace("Everyone", np.nan)
data['Price'] = data.Price.str.replace("$","")
data['Price'] = data['Price'].astype(float)


# In[27]:


data["Price"].dtype


# In[28]:


data.head(2)


# In[29]:


data['Last Updated'].unique()


# # Data Visualization

# In[113]:


import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mp


# In[32]:


data.describe()


# In[33]:


data.corr()


# In[34]:


f,ax = plt.subplots(figsize=(12,12))
sns.heatmap(data.corr(), annot=True, linewidths=.5, fmt='.1f',ax=ax)
plt.show()


# In[35]:


category_list = list(data['Category'].unique())
category_review = []
for i in category_list:
    x = data[data['Category'] == i]
    if (len(x)!=0):
        review = sum(x.Reviews)/len(x)
        category_review.append(review)
    else:
        review = sum(x.Reviews)
        category_review.append(review)
        
data_category_reviews = pd.DataFrame({'Category': category_list, 'review':category_review})
new_index = (data_category_reviews['review'].sort_values(ascending=False)).index.values
sorted_data = data_category_reviews.reindex(new_index)


# In[36]:


plt.figure(figsize=(15,10))
sns.barplot(x=sorted_data['Category'], y=sorted_data['review'])
plt.xticks(rotation=85)
plt.xlabel("Category")
plt.ylabel("Reviews")
plt.title("Category and Reviews")
plt.show()


# Observation:- Communication and social have more reviews among all category

# In[37]:


category_list = list(data['Category'].unique())
category_install = []
for i in category_list:
    x = data[data['Category'] == i]
    if (len(x)!=0):
        install = sum(x.Installs)/len(x)
        category_install.append(install)
    else:
        install = sum(x.Installs)
        category_install.append(install)
        
data_category_install = pd.DataFrame({'Category': category_list, 'install':category_install})
new_index = (data_category_install['install'].sort_values(ascending=False)).index.values
sorted_data = data_category_install.reindex(new_index)


# In[38]:


plt.figure(figsize=(15,10))
sns.barplot(x=sorted_data['Category'], y=sorted_data['install'])
plt.xticks(rotation=85)
plt.xlabel("Category")
plt.ylabel("Installs")
plt.title("Category and Installs")
plt.show()


# Observation:- Communication category apps has highest Installs followed by Social and Medical has least installs among the category 

# In[39]:


plt.figure(figsize=(10,7))
sns.countplot(data=data, x= 'Content Rating')
plt.xticks(rotation=85)
plt.title('Content Rating', color='red', fontsize =15)
plt.show()


# In[ ]:





# In[40]:


top_genres = data.Genres.value_counts().reset_index().rename(columns={'Genres':'Count','index':'Genres'})
genres_installs = data.groupby(['Genres'])['Installs'].sum()
top_genres_installs = pd.merge(top_genres,genres_installs, on = "Genres")
top_20_genres_installs = top_genres_installs.head(20)


# In[41]:


plt.figure(figsize=(14,7))
plt.xticks(rotation=75)
plt.xlabel("Genres")
plt.ylabel("Number of application")
plt.title("top 20 Genres")
sns.barplot(top_20_genres_installs.Genres, top_20_genres_installs.Count)
plt.show()


# Observation:- Tools genres has the highest number of apps among all.

# In[42]:


plt.figure(figsize=(14,7))
plt.xticks(rotation=60)
plt.xlabel("Genres")
plt.ylabel("Installs")
plt.title("Installs according to genre")
sns.barplot(top_20_genres_installs.Genres, top_20_genres_installs.Installs)
plt.show()


# Observation:- Communication genres has the highest number of installs among the category.

# In[43]:


genres_rating_df = data.groupby(['Genres'])["Rating"].mean()
genres_installs_ratings = pd.merge(top_genres_installs, genres_rating_df, on="Genres")
genres_installs_ratings['Rating'].describe()


# In[44]:


plt.figure(figsize=(14,7))
g = sns.kdeplot(genres_installs_ratings.Rating, color = "Red", shade = True)
g.set_xlabel("Rating")
g.set_ylabel("Frequency")
plt.title('Distribution of rating', size=20)


# In[55]:


genres_installs_ratings.sort_values('Rating', ascending = False, inplace = True)
highest_rated_genres = genres_installs_ratings.iloc[0:20]
lowest_rated_genres = genres_installs_ratings.iloc[-20:]
lowest_rated_genres = lowest_rated_genres[lowest_rated_genres['Rating'].notnull()]


# In[54]:


plt.figure(figsize=(14,7))
plt.xticks(rotation=65)
plt.xlabel("Genres")
plt.ylabel("Rating")
plt.title("Ratings according to title")
sns.barplot(highest_rated_genres.Genres, highest_rated_genres.Rating)
plt.show()


# In[58]:


plt.figure(figsize=(14,7))
plt.xticks(rotation=65)
plt.xlabel("Genres")
plt.ylabel("Rating")
plt.title("Ratings according to genres")
sns.barplot(lowest_rated_genres.Genres, lowest_rated_genres.Rating)
plt.show()


# In[65]:


app_count = data.groupby(["Category", "Type"])[['App']].count().reset_index().rename(columns={'App':'Count', 'index':'App'})
df_app_count = app_count.pivot('Category','Type','Count').fillna(0).reset_index()
df_app_count.set_index('Category').plot(kind='bar', stacked=True, figsize=(18,9))
plt.xlabel('Category', fontsize=15)
plt.ylabel('Count',fontsize=15)
plt.title("Count of application in each category according to types")
plt.show()


# Observation:- Family category has the most number of free and paid apps followed by games category

# In[76]:


data['Gaming category app'] = data['Category'] =='Game'
category_type_installs = data.groupby(['Category','Type'])[['Installs']].sum().reset_index()
category_type_installs['Log_installs'] = np.log10(category_type_installs["Installs"])
plt.figure(figsize=(18,9))
plt.xticks(rotation=65, fontsize=9)
plt.xlabel('Category')
plt.ylabel('Installs(base10)')
plt.title('Number of installs(base10) type wise according to Category')
sns.barplot("Category","Log_installs", hue='Type', data=category_type_installs);
plt.show()


# In[77]:


data.loc[data['Size'].isnull(), 'Size']=0


# In[78]:


plt.xlabel("Size")
plt.title("Distribution of size")
plt.hist(data['Size']);
plt.show()


# Observation:- Most number of apps are more than 5MB of size

# In[82]:


#Merging data of user review
user_review


# In[101]:


merge_df=data.merge(user_review, on="App")
Category_sentiment = merge_df.groupby(['Category','Sentiment']).size().reset_index(name='Sentiment count')
Category_sentiment['Lg_sentiment_count']=np.log2(Category_sentiment['Sentiment count'])
plt.figure(figsize=(16,8))
plt.xticks(rotation=90, fontsize=11)
plt.xlabel("Category", fontsize=15)
plt.ylabel("Installs", fontsize=15)
plt.title("Number of installs type according to genre", fontsize=15)
sns.barplot("Category", "Lg_sentiment_count", hue="Sentiment", data=Category_sentiment)
plt.show()


# Observation:- Game category has the most number of Positive, Negative and Neutral reviews.

# In[110]:


plt.figure(figsize=(16,8))
plt.xticks(rotation=85, fontsize=15)
plt.title("Distribution of subjectivity")
plt.xlabel("Subjectivity")
plt.hist(merge_df[merge_df['Sentiment_Subjectivity'].notnull()]['Sentiment_Subjectivity'])
plt.show()


# In[123]:


counts = list(merge_df['Sentiment'].value_counts())
labels = 'Positive Reviews','Negative Reviews','Neutral Reviews'
mp.rcParams['font.size']=12
mp.rcParams['figure.figsize']=(8,8)
plt.pie(counts, labels=labels, explode=[0,0.5,0.005], shadow=True, autopct="%.2f%%")
plt.title("Pie chart representing percentage of review sentiments", fontsize=20)
plt.axis('off')
plt.legend()
plt.show()


# In[ ]:




