import requests
from selectolax.parser import HTMLParser


def main(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    html_content = response.text

    with open("amazon.html", "w") as f:
        f.write(html_content)

    tree = HTMLParser(html_content)
    price_node = tree.css_first("span.a-price-whole")
    return int(price_node.text().replace(",", ""))


if __name__ == '__main__':
    import time

    asin = "B0B46N7QQL"
    url = f"https://www.amazon.fr/dp/{asin}"
    for i in range(10):
        print(main(url))
        time.sleep(0.5)
