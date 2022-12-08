from flask import Flask
from crawler import WebCrawler
from preprocess import read_data
from preprocess import data_split
from preprocess import clean_data
from rank import Ranker
import operator
import json

app = Flask(__name__)

data_path = "cw.txt"

def crawl():
    crawler = WebCrawler()
    crawler.set_up()
    crawler.scrap_page()
    crawler.close()

@app.route("/<keyword>")
def main(keyword):
    # step 1: crawl the page
    crawl() 

    # step 2: clean the data and categorize
    post_data = read_data(data_path)
    labeled_data, unlabeled_data = data_split(post_data)

    post_store = {}
    for post in post_data:
        post_id = post[0]
        post_store[post_id] = {}
        post_store[post_id]["post_title"] = post[2]
        post_store[post_id]["post_content"] = post[3]

    # step 3: index and rank
    # ranker = Ranker(unlabeled_data)
    ranker = Ranker(post_data)
    ranker.index()
    for i in ranker.inverted_index:
        print(i)
        print(ranker.inverted_index[i])
    keyword = clean_data(keyword)
    ranker.computeScore(keyword)

    # step 4: get the top five post
    ranker.score = sorted(ranker.score.items(),key=operator.itemgetter(1),reverse=True)
    n_post_ids = [post[0] for post in ranker.score][:5]
    json_data = {}
    data = []
    for post_id in n_post_ids:
        object = {}
        object["id"] = post_id
        object["title"] = post_store[post_id]["post_title"]
        object["content"] = post_store[post_id]["post_content"]
        data.append(object)
    json_data["data"] = data
    return json.dumps(json_data)