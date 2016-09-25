import requests
import sys

from bs4 import BeautifulSoup
from urllib.parse import quote_plus


search_url = ("https://www.ultimate-guitar.com/"
              "search.php?search_type=title&value={query}")


def get_search_url(query):
    return search_url.format(query=quote_plus(query))


def get_tabs_for_search(search_query):
    print("Searching for query: {}".format(search_query))

    url = get_search_url(search_query)
    print(url)
    r = requests.get(url)

    soup = BeautifulSoup(r.text, "lxml")
    print(soup)
    result_lines = soup.findAll(
        attrs={"class": "tresults"})[0].findAll('tr')[1:]

    result_list = []

    artist = ""
    for result_line in result_lines:
        tds = result_line.findAll('td')

        curr_artist = tds[0].text.strip()
        artist = curr_artist if curr_artist else artist

        # get and check the tab type
        tab_type = tds[-1].strong.text

        if tab_type not in ['chords', 'tab']:
            continue

        link = tds[1].findAll(
            "a", attrs={"class": "song result-link"})[0]['href']

        result_list.append((artist, "name", tab_type, link))

        # print("artist: {}\nlink:{}\ntab_type: {}".format(
        #    artist, link, tab_type))

    return result_list


def main():
    result = get_tabs_for_search("all too well")

    print(result)


if __name__ == '__main__':
    main()
