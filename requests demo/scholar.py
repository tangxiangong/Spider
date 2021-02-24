#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Time : 2021/2/24 15:47

import requests


url = r'https://scholar.google.com/scholar?q='
headers = {
"Host" : "scholar.google.com",
"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15"
}
params = {
    'q': '"fractional Brownian motion"',
    "start": "0",
    "as_sdt": "0,5"
}
response = requests.get(url, headers=headers, params=params)
print(response.status_code)
