from threading import Thread
import pandas as pd
import requests
from http import HTTPStatus


class CustomThread(Thread):
    def __init__(self, func, args):
        super(CustomThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None

def get_invalid_url_set():
    tmdb_df = pd.read_csv('./imdb_top_1000.csv')
    def validate_img_link(link):
        if requests.head(link).status_code != HTTPStatus.OK:
            return link
        return None
    thread_list = []
    ret = set()
    for _, row in tmdb_df.iterrows():
        thread_list.append(CustomThread(validate_img_link, args=(row['Poster_Link'],)))
    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()
    for t in thread_list:
        if t.get_result():
            ret.add(t.get_result())
    return ret
