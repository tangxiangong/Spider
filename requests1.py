import requests


if __name__ == "__main__":
    url = r'https://www.google.com/'
    request = requests.get(url=url)
    text = request.text
    with open("./google.html", 'w', encoding='utf-8') as f:
        f.write(text)
