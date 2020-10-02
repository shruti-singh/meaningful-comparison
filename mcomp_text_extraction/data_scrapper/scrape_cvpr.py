from collections import defaultdict
import requests
from bs4 import BeautifulSoup

def part_zero():

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
        }

    url = "https://openaccess.thecvf.com/menu"
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, "html.parser")

    yearwise_pages = []
    links = soup.find_all("a")
    for l in links:
        href_text = l.get("href")
        if href_text and href_text.find("CVPR") > -1:
            yearwise_pages.append(href_text)


    paper_urls = defaultdict(list)
    for yp in yearwise_pages:
        print("Page: ", yp)
        if not yp.find("workshop") > -1:
            year_url = "https://openaccess.thecvf.com/" + yp
            req = requests.get(year_url, headers)
            soup = BeautifulSoup(req.content, "html.parser")

            links = soup.find_all("a")
            conf_day_links = []

            for l in links:
                href_text = l.get("href")
                if href_text and href_text.endswith("day") > -1:
                    conf_day_links.append(href_text)
            # print("Number of conf days: ", conf_day_links)

            ind_links = False
            if yp.find("2017") > -1 or yp.find("2016") > -1 or yp.find("2015") > -1 or yp.find("2014") > -1 or yp.find("2013") > -1:
                for l in links:
                    href_text = l.get("href")
                    if href_text and href_text.endswith("pdf") > -1:
                        ind_links = True
                        conf_day_links.append(href_text)
                # conf_day_links = links.copy()

            for c in conf_day_links:
                if ind_links:
                    if c.endswith(".pdf"):
                        paper_urls["https://openaccess.thecvf.com/"].append(c)
                    else:
                        if c.endswith(".html"):
                            c = c.replace(".html", ".pdf")
                            c = c.replace("/html/", "/papers/")
                            paper_urls["https://openaccess.thecvf.com/"].append(c)
                        elif not href_text == "#":
                            print(c)
                    continue
                req = requests.get("https://openaccess.thecvf.com/" + c, headers)
                soup = BeautifulSoup(req.content, "html.parser")
                links = soup.find_all("a")
                # print("Each days papers links: ", links[0:20])
                for l in links:
                    href_text = l.get("href")
                    if href_text and href_text.endswith(".html"):
                        href_text = href_text.replace("html", "pdf")
                        href_text = href_text.replace("/pdf/", "/papers/")
                        if not (href_text.find("/supplemental/") > -1 or href_text.endswith("/#")):
                            if href_text.endswith(".pdf"):
                                paper_urls["https://openaccess.thecvf.com/"].append(href_text)
                            else:
                                if href_text.endswith(".html"):
                                    href_text = href_text.replace(".html", ".pdf")
                                    href_text = href_text.replace("/html/", "/papers/")
                                    paper_urls["https://openaccess.thecvf.com/"].append(href_text)
                                elif not href_text == "#":
                                    print(href_text)
                        # req = requests.get("https://openaccess.thecvf.com/" + href_text, headers)
                        # soup = BeautifulSoup(req.content, "html.parser")
                        # paper_specific_urls = soup.find_all("a")
                        # print(paper_specific_urls)
                        # for purl in paper_specific_urls:
                        #     paperspec_href = purl.get("href")
                        #     if paperspec_href and paperspec_href.endswith(".pdf"):
                        #         paper_urls["https://openaccess.thecvf.com/"].append(paperspec_href)
        else:
            # try:
            workshops_url = "https://openaccess.thecvf.com" + yp
            req = requests.get(workshops_url, headers)
            soup = BeautifulSoup(req.content, "html.parser")

            workshop_pages = []
            links = soup.find_all("a")
            for l in links:
                href_text = l.get("href")
                if href_text and href_text.find("CVPR") > -1:
                    workshop_pages.append(href_text)
            for w in workshop_pages:
                req = requests.get(workshops_url.replace("menu.py", "") + w, headers)
                soup = BeautifulSoup(req.content, "html.parser")
                links = soup.find_all("a")
                for l in links:
                    href_text = l.get("href")
                    if href_text and href_text.endswith(".html"):
                        href_text = href_text.replace("html", "pdf")
                        href_text = href_text.replace("/pdf/", "/papers/")
                        if not (href_text.find("/supplemental/") > -1 or href_text.endswith("/#")):
                            if href_text.endswith(".pdf"):
                                paper_urls["https://openaccess.thecvf.com/"].append(href_text)
                            else:
                                if href_text.endswith(".html"):
                                    href_text = href_text.replace(".html", ".pdf")
                                    href_text = href_text.replace("/html/", "/papers/")
                                    paper_urls["https://openaccess.thecvf.com/"].append(href_text)
                                elif not href_text == "#":
                                    print(href_text)
            # except Exception as ex:
            #     print("Ex: ", ex)

    print("Len of links dict: {}".format(len(paper_urls)))
    print("Total len of links dict: {}".format(len(paper_urls.items())))
    # print(paper_urls)

    with open("cvpr_paper_urls.txt", "w") as f:
        for k in paper_urls:
            for v in paper_urls[k]:
                f.write(k + v + "\n")


def part_one():
    # "Remove duplicate urls occurring due to .html and .pdf co-occurences. Also adding arxiv links from errscvpr"
    paper_urls = []
    with open("cvpr_paper_urls.txt", "r") as f:
        dups = f.readlines()
    unique_urls = set(dups)

    with open("errscvpr", "r") as f:
        all_junk = f.readlines()

    for l in all_junk:
        if l.find("arxiv.org") > -1:
            unique_urls.add(l)

    with open("cvpr_paper_urls_updated.txt", "w") as f:
        for l in unique_urls:
            f.write(l.strip() + "\n")
    return


if __name__ == "__main__":
    # part_zero()
    part_one()