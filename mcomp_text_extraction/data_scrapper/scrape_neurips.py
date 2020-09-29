from collections import defaultdict
import requests
from bs4 import BeautifulSoup

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

url = "https://papers.nips.cc/"
req = requests.get(url, headers)
soup = BeautifulSoup(req.content, "html.parser")

yearwise_pages = []
links = soup.find_all("a")
for l in links:
    href_text = l.get("href")
    if href_text.find("neural") > -1:
        yearwise_pages.append(href_text)


paper_urls = defaultdict(list)
for yp in yearwise_pages:
    year_url = url[:-1] + yp
    req = requests.get(year_url, headers)
    soup = BeautifulSoup(req.content, "html.parser")

    links = soup.find_all("a")
    for l in links:
        href_text = l.get("href")
        if href_text.startswith("/paper"):
            paper_urls[year_url].append(href_text)

with open("neurips_paper_urls.txt", "w") as f:
    for k in paper_urls:
        for v in paper_urls[k]:
            f.write(k + v + "\n")