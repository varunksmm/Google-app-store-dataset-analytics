import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mp


def data_describe(data):
    # print(data.describe())
    f, ax = plt.subplots(figsize=(12, 12))
    sns.heatmap(data.corr(), annot=True, linewidths=.5, fmt='.1f', ax=ax)
    plt.show()


def visual_category_reviews(data):
    category_list = list(data['Category'].unique())
    category_review = []
    for i in category_list:
        x = data[data['Category'] == i]
        if len(x) != 0:
            review = sum(x.Reviews) / len(x)
            category_review.append(review)
        else:
            review = sum(x.Reviews)
            category_review.append(review)

    data_category_reviews = pd.DataFrame({'Category': category_list, 'review': category_review})
    new_index = (data_category_reviews['review'].sort_values(ascending=False)).index.values
    sorted_data = data_category_reviews.reindex(new_index)

    plt.figure(figsize=(15, 10))
    sns.barplot(x=sorted_data['Category'], y=sorted_data['review'])
    plt.xticks(rotation=85)
    plt.xlabel("Category")
    plt.ylabel("Reviews")
    plt.title("Category and Reviews")
    plt.show()


def visual_category_install(data):
    category_list = list(data['Category'].unique())
    category_install = []
    for i in category_list:
        x = data[data['Category'] == i]
        if len(x) != 0:
            install = sum(x.Installs) / len(x)
            category_install.append(install)
        else:
            install = sum(x.Installs)
            category_install.append(install)

    data_category_install = pd.DataFrame({'Category': category_list, 'install': category_install})
    new_index = (data_category_install['install'].sort_values(ascending=False)).index.values
    sorted_data = data_category_install.reindex(new_index)

    plt.figure(figsize=(15, 10))
    sns.barplot(x=sorted_data['Category'], y=sorted_data['install'])
    plt.xticks(rotation=85)
    plt.xlabel("Category")
    plt.ylabel("Installs")
    plt.title("Category and Installs")
    plt.show()


def visual_content_count(data):
    plt.figure(figsize=(10, 7))
    sns.countplot(data=data, x='Content Rating')
    plt.xticks(rotation=85)
    plt.title('Content Rating', color='red', fontsize=15)
    plt.show()


def get_top_20_data(data):
    return top_genres_installs(data).head(20)


def top_genres_installs(data):
    top_genres = data.Genres.value_counts().reset_index().rename(columns={'Genres': 'Count', 'index': 'Genres'})
    genres_installs = data.groupby(['Genres'])['Installs'].sum()
    top_genres_installs = pd.merge(top_genres, genres_installs, on="Genres")
    return top_genres_installs


def visual_top20_genre(data):
    top_20 = get_top_20_data(data)
    plt.figure(figsize=(14, 7))
    plt.xticks(rotation=75)
    plt.xlabel("Genres")
    plt.ylabel("Number of application")
    plt.title("top 20 Genres")
    sns.barplot(top_20.Genres, top_20.Count)
    plt.show()


def visual_genre_instal(data):
    top_20 = get_top_20_data(data)
    plt.figure(figsize=(14, 7))
    plt.xticks(rotation=60)
    plt.xlabel("Genres")
    plt.ylabel("Installs")
    plt.title("Installs according to genre")
    sns.barplot(top_20.Genres, top_20.Installs)
    plt.show()


def visual_rating_freq(data):
    # top_20 = get_top_20_data(data)
    genres_rating_df = data.groupby(['Genres'])["Rating"].mean()
    genres_installs_ratings = pd.merge(top_genres_installs(data), genres_rating_df, on="Genres")
    plt.figure(figsize=(14, 7))
    g = sns.kdeplot(genres_installs_ratings.Rating, color="Red", shade=True)
    g.set_xlabel("Rating")
    g.set_ylabel("Frequency")
    plt.title('Distribution of rating', size=20)
    plt.show()


def visual_data_category(data):
    app_count = data.groupby(["Category", "Type"])[['App']].count().reset_index().rename(
        columns={'App': 'Count', 'index': 'App'})
    df_app_count = app_count.pivot('Category', 'Type', 'Count').fillna(0).reset_index()
    df_app_count.set_index('Category').plot(kind='bar', stacked=True, figsize=(18, 9))
    plt.xlabel('Category', fontsize=15)
    plt.ylabel('Count', fontsize=15)
    plt.title("Count of application in each category according to types")
    plt.show()


def visual_category_gaming(data):
    data['Gaming category app'] = data['Category'] == 'Game'
    category_type_installs = data.groupby(['Category', 'Type'])[['Installs']].sum().reset_index()
    category_type_installs['Log_installs'] = np.log10(category_type_installs["Installs"])
    plt.figure(figsize=(18, 9))
    plt.xticks(rotation=65, fontsize=9)
    plt.xlabel('Category')
    plt.ylabel('Installs(base10)')
    plt.title('Number of installs(base10) type wise according to Category')
    sns.barplot("Category", "Log_installs", hue='Type', data=category_type_installs);
    plt.show()


def visual_distribution_size(data):
    plt.xlabel("Size")
    plt.title("Distribution of size")
    plt.hist(data['Size'])
    plt.show()


def visual_merge_category_sentiment(data, review_data):
    merge_df = data.merge(review_data, on="App")
    Category_sentiment = merge_df.groupby(['Category', 'Sentiment']).size().reset_index(name='Sentiment count')
    Category_sentiment['Lg_sentiment_count'] = np.log2(Category_sentiment['Sentiment count'])
    plt.figure(figsize=(16, 8))
    plt.xticks(rotation=90, fontsize=11)
    plt.xlabel("Category", fontsize=15)
    plt.ylabel("Installs", fontsize=15)
    plt.title("Number of installs type according to genre", fontsize=15)
    sns.barplot("Category", "Lg_sentiment_count", hue="Sentiment", data=Category_sentiment)
    plt.show()


def visual_ditribution_subjectivity(data, review_data):
    merge_df = data.merge(review_data, on="App")
    plt.figure(figsize=(16, 8))
    plt.xticks(rotation=85, fontsize=15)
    plt.title("Distribution of subjectivity")
    plt.xlabel("Subjectivity")
    plt.hist(merge_df[merge_df['Sentiment_Subjectivity'].notnull()]['Sentiment_Subjectivity'])
    plt.show()


def visual_sentiment(data, review_data):
    merge_df = data.merge(review_data, on="App")
    counts = list(merge_df['Sentiment'].value_counts())
    labels = 'Positive Reviews', 'Negative Reviews', 'Neutral Reviews'
    mp.rcParams['font.size'] = 12
    mp.rcParams['figure.figsize'] = (8, 8)
    plt.pie(counts, labels=labels, explode=[0, 0.5, 0.005], shadow=True, autopct="%.2f%%")
    plt.title("Pie chart representing percentage of review sentiments", fontsize=20)
    plt.axis('off')
    plt.legend()
    plt.show()
