#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Time : 2021/2/24 15:47
import os
import requests


class Scholar(object):
    url = r'https://scholar.google.com/scholar?q='
    headers = {
        "Host": "scholar.google.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15"
    }

    def __init__(self, query: str):
        """
        :param query:
        """
        self.query = query
        self.params = {
            'q': f'"{self.query}"',
            "start": "0",
            "as_sdt": "0,5"
        }
        self.state = True

    def _search_one_page(self) -> str:
        response = requests.get(Scholar.url, headers=Scholar.headers, params=self.params)
        if response.status_code == 200:
            print("Connect Successfully!")
            self.state = True
            return response.text
        else:
            print("Connect Failed!!!")
            self.state = False
            return ""

    def _save_html(self, root=None):
        if not self.state:
            print("Error")
            return
        else:
            text = self._search_one_page()
        if root is None:
            root = os.getcwd()
        if os.path.exists(root):
            path = os.path.join(root, f"{self.query}.html")
            print(f"The html file is stored in the {root} and its name is '{self.query}.html'.")
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
        else:
            print("Error. The root do not exist.")
            return

    def search(self):
        self._save_html()
    # TODO: 当前只是搜索了第一页的内容，给参数self.params['start']做一个计时器以搜索任意页数。


if __name__ == "__main__":
    s = Scholar("random walk")
    s.search()
