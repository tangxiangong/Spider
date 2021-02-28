#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Time : 2021/2/24 15:47
import os
# import re
import time
import shutil
import requests
import numpy as np
from bs4 import BeautifulSoup


def _set_root(root: str) -> str:
    if root is None:
        return os.getcwd()
    else:
        return root


def _mkdir(root: str):
    if os.path.exists(root):
        shutil.rmtree(root)
    os.mkdir(root)


class Scholar(object):
    _url = r'https://scholar.google.com/scholar?hl=zh-CN&q='
    _headers = {
        "Host": "scholar.google.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) "
        + "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15"
    }

    def __init__(self, query: str, pages: int = 1, root: str = None):
        """
        :param query:
        """
        self._current_page = 1
        self._query = query
        self._pages = pages
        self._params = {
            'q': f'"{self._query}"',
            "start": "0",
            "as_sdt": "0,5"
        }
        self._root = _set_root(root=root)
        assert self._test_root() and self._test_connection()
        self._root = os.path.join(self._root, f"{self._query}")
        _mkdir(self._root)
        self._html_root = os.path.join(self._root, "html")
        _mkdir(self._html_root)
        self._html = []
        self._papers_url_list = np.zeros((self._pages, 10), dtype=str)

    def _test_connection(self) -> bool:
        response = requests.get(Scholar._url, headers=Scholar._headers, params=self._params)
        if response.status_code == 200:
            return True
        else:
            print("ERROR")
            return False

    def _test_root(self) -> bool:
        if os.path.exists(self._root):
            return True
        else:
            print("ERROR!")
            return False

    def _search_one_page(self):
        response = requests.get(Scholar._url, headers=Scholar._headers, params=self._params)
        assert response.status_code == 200
        self._html.append(response.text)

    def _save_html_file(self):
        self._search_one_page()
        path = os.path.join(self._html_root, f"{self._query}_page_{self._current_page}.html")
        with open(path, 'w', encoding='utf-8') as f:
            f.write(self._html[-1])

    def _update_params(self):
        self._params = {
            'as_vis': '1',
            'q': f'"{self._query}"',
            "start": str((self._current_page - 1) * 10),
            "as_sdt": "0,5"
        }

    def _next_page(self):
        self._current_page += 1
        self._update_params()
        time.sleep(2)
        self._save_html_file()

    def _save_html_files(self):
        self._save_html_file()
        for _ in range(1, self._pages):
            self._next_page()

    def search(self):
        self._save_html_files()

    def get_html_root(self):
        return self._html_root

    # def _get_papers_url_list(self):
    #     pattern = re.compile(r'<div class="gs_ri">.*?<a .*?href="(.*?)"')
    #     for i in range(0, self._pages):
    #         self._papers_url_list[i] = pattern.findall(self._html[i], re.S)
    #
    # def show_url(self):
    #     self._get_papers_url_list()
    #     print(self._papers_url_list)


if __name__ == "__main__":
    s = Scholar("L1 method")
    s.search()
    # s.show_url()
