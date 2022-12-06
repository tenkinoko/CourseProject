
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import re
import math

stop_words = set(stopwords.words('english'))
stemmer = SnowballStemmer('english')

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

class Ranker:

    def __init__(self, unlabeled_data):
        self.unlabeled_posts = unlabeled_data
        self.inverted_index = {}
        self.doc_length = {}
        self.avg_doc_length = 0
        self.score = {}

    # build inverted index for general posts
    def index(self):
        doc_length_sum = 0
        for post in self.unlabeled_posts:
            post_id = post[0]
            self.doc_length[post_id] = len(post[3])
            doc_length_sum += len(post[3])
            clean_post = clean_data(post[3]) 

            for word in clean_post:
                if word not in self.inverted_index:
                    postings = {}
                    postings[post_id] = 1
                    self.inverted_index[word] = {'term_frequency' : 1, 
                                        'doc_frequency' : 1,
                                        'postings' : postings
                                        }
                else:
                    self.inverted_index[word]['term_frequency'] += 1
                    if word in self.inverted_index[word]['postings']:
                        self.inverted_index[word]['postings'][post_id] += 1
                    else:
                        self.inverted_index[word]['postings'][post_id] = 1

        self.avg_doc_length = doc_length_sum / len(self.unlabeled_posts)

    # get term frequency of a word in a post
    def get_term_frequency(self, word, post_id):
        try:
            term_frequency = self.inverted_index[word]['postings'][post_id] 
            return term_frequency
        except:
            return 0


    # get doc frequency of a word
    def get_doc_frequency(self, word):
        if word in self.inverted_index:
            return len(self.inverted_index[word]['postings'])
        else:
            raise 0

    # compute score of each post given the query
    def computeScore(self, query):
        k = 1.25
        b = 0.75
        for post in self.unlabeled_posts:
            score = 0
            post_id = post[0]
            for word in query:
                term_frequency = self.get_term_frequency(word, post_id)
                doc_length = self.doc_length[post_id]
                idf = self.computeIDF(word)
                term_score = (term_frequency * (k + 1)) / (term_frequency + k * (1 - b + b * (doc_length / self.avg_doc_length)))
                term_score *= idf
                score += term_score
            self.score[post_id] = score

    # compute idf
    def computeIDF(self, word):
        doc_frequency = self.get_doc_frequency(word)
        idf = math.log((len(self.unlabeled_posts) - doc_frequency + 0.5) / (doc_frequency + 0.5))
        return idf
