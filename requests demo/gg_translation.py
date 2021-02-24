import requests
# 需要解密


def en2zh(word: str):
    url = r"https://translate.google.com/_/TranslateWebserverUi/data/batchexecute?rpcids=MkEWBc&f.sid=-3400012625141294965&bl=boq_translate-webserver_20210222.14_p0&hl=zh-CN&soc-app=1&soc-platform=1&soc-device=1&_reqid=858394&rt=c"
    headers = {
        "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15"
    }
    data = {
        "f.req": f'[[["MkEWBc", "[[\"{word}\",\"en\",\"zh-CN\",true],[null]]", null, "generic"]]'
    }
    response = requests.post(url, data=data, headers=headers)
    print(response.status_code)
    return

if __name__ == "__main__":
    en2zh("calculus")