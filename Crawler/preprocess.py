import numpy as np
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from mysutils.text import remove_urls
from nltk.stem import SnowballStemmer, WordNetLemmatizer
# from string import punctuation
import re

stop_words = set(stopwords.words('english'))
data_path = "cw.txt"
stemmer = SnowballStemmer('english')


# load the Campuswire posts crawled
# Format: [PostID, Category, Title, Content]
def read_data(filepath):
    post_file = open(filepath, "r+")
    post = post_file.readlines()
    for i in range(len(post)):
        post[i] = remove_urls(post[i]).rstrip('\n')
    post = np.array(post).reshape(-1, 4)
    return post


# remove non-English words and stop words
def clean_data(txt, is_stem=False):
    txt = re.sub('[0-9]', '', txt)
    txt = txt.lower()
    txt = re.sub('[^a-zA-Z]', ' ', txt)
    word_tokens = word_tokenize(txt)
    if is_stem:
        filtered_word = [stemmer.stem(w) for w in word_tokens if w not in stop_words]
    else:
        filtered_word = [w for w in word_tokens if w not in stop_words]
    return filtered_word


# filter the data whose category is 'General' for further categorization
def data_split(data):
    labeled = data[np.where(data != 'General')[0], :]
    unlabeled = data[np.where(data == 'General')[0], :]
    return labeled, unlabeled


if __name__ == "__main__":
    post_data = read_data(data_path)
    labeled_data, unlabeled_data = data_split(post_data)
    print(unlabeled_data)