import re
import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []

    # parse and create scores list
    poins = parser.find_all("span", attrs={"class": "score"})
    poins_list = [score.text.split()[0] for score in poins]

    # parse and create authors list
    authors = parser.find_all("a", attrs={"class": "hnuser"})
    authors_list = [author.text for author in authors]     

    # parse and create urls list, titles list
    data = parser.find_all("a", attrs={"class": "storylink"})
    urls_list = [url['href'] for url in data]
    titles_list = [title.text for title in data]

    # parse and create comments list
    items = parser.find_all("td", attrs={"class": "subtext"})
    comments_list = []
    for item in items:
        for tag in item.find_all("a", attrs={"href": True}):
            # if doesn't has comments, tag.text after anchor (which has text = "web") is "discuss"
            if tag.text == "discuss":
                comments_list.append('0')
            # if has comments, amount of comments was dynamically displayed
            # so need to find amount of comments like bellow
            if 'comment' in tag.text:
                cmt = re.findall('\d+', tag.text)
                comments_list.append(cmt[0])

    news_list = [{"author": a, "comments": c, "points": p, "title": t, "url": u}
                 for a, c, p, t, u in zip(authors_list, comments_list, poins_list, titles_list, urls_list)]

    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    link = parser.find("a", attrs={"class": "morelink"})
    return link['href']


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news


if __name__ == "__main__":
    news_list = get_news("https://news.ycombinator.com/newest", n_pages=2)

