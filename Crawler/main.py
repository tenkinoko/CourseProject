from crawler import WebCrawler
from preprocess import read_data
from preprocess import data_split
from preprocess import clean_data
from rank import Ranker
import operator

data_path = "cw.txt"

def crawl():
    crawler = WebCrawler()
    crawler.set_up()
    crawler.scrap_page()
    crawler.close()

def get_query():
    return "grade"

def rank(ranker):
    ranker.index()
    query = get_query()
    query = clean_data(query)
    ranker.computeScore(query)

if __name__ == '__main__':
    # step 1: crawl the page
    # crawl() 

    # step 2: clean the data and categorize
    post_data = read_data(data_path)
    labeled_data, unlabeled_data = data_split(post_data)
    print(unlabeled_data)

    # step 3: index and rank
    ranker = Ranker(unlabeled_data)
    rank(ranker)

    # step 4: get the top five post
    ranker.score = sorted(ranker.score.items(),key=operator.itemgetter(1),reverse=True)
    n_items = [post[0] for post in ranker.score][:5]
    print(n_items)