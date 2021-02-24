import requests


def search(query: str):
    gg = r"https://www.google.com/search?q="
    headers = {
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15"
    }
    print(f"Searching {query} ...")
    url = gg + query
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        print("Success!!!")
        with open(f"gg_search_{query}.html", 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"The result is stored in gg_search_{query}.html.")
    else:
        print("Failed")
    return


if __name__ == "__main__":
    search("China")