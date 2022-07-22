from files.data_cleaning import data_cleaning
from files.data_visualization import visual_category_gaming, visual_distribution_size, visual_merge_category_sentiment, \
    visual_ditribution_subjectivity, visual_sentiment, data_describe, visual_category_reviews, visual_category_install, \
    visual_content_count, visual_top20_genre, visual_genre_instal, visual_rating_freq, visual_data_category
from files.file_import import get_apps_data, get_review_data


def start():
    data = get_apps_data()
    review_data = get_review_data()
    data_cleaning(data)
    data_describe(data)
    visual_category_reviews(data)
    visual_category_install(data)
    visual_content_count(data)
    visual_top20_genre(data)
    visual_genre_instal(data)
    visual_rating_freq(data)
    visual_data_category(data)
    visual_category_gaming(data)
    visual_distribution_size(data)
    visual_merge_category_sentiment(data, review_data)
    visual_ditribution_subjectivity(data, review_data)
    visual_sentiment(data, review_data)


if __name__ == '__main__':
    start()
