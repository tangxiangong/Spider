#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Time : 2021/2/24 15:47
import os
import time
import shutil
import requests
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


def _one_page_urls_and_titles(html):
    soup = BeautifulSoup(html, 'lxml')
    temp = soup.select('.gs_rt a')
    assert len(temp) == 10
    url = ['' for _ in range(10)]
    title = ['' for _ in range(10)]
    for index, tp in enumerate(temp):
        url[index] = tp['href']
        title[index] = tp.text
    return url, title


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
        self._save_html_files()
        self._papers_url_list = [['' for _ in range(10)] for __ in range(self._pages)]
        self._papers_title_list = [['' for _ in range(10)] for __ in range(self._pages)]
        self._get_papers_url_and_title_list()

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

    # def search(self):
        # self._save_html_files()

    # def get_html_root(self):
    #     return self._html_root

    def _get_papers_url_and_title_list(self):
        for k in range(self._pages):
            self._papers_url_list[k], self._papers_title_list[k] = _one_page_urls_and_titles(self._html[k])

    def get_url(self):
        return self._papers_url_list

    def get_title(self):
        return self._papers_title_list


if __name__ == "__main__":
    p = 2
    s = Scholar("L1 method", pages=p)
    u = s.get_url()
    t = s.get_title()
    with open('data.txt', 'w', encoding='utf-8') as fp:
        for i in range(p):
            fp.writelines(f"第{i+1}页:\n")
            for j in range(10):
                if j < 9:
                    fp.writelines(f"{j+1}. title: {t[i][j]}\n   url: {u[i][j]}\n\n")
                else:
                    fp.writelines(f"{j+1}. title: {t[i][j]}\n    url: {u[i][j]}\n\n")
