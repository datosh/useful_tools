import requests
import sys

from bs4 import BeautifulSoup
from urllib.parse import quote_plus


search_url = "https://www.ultimate-guitar.com/search.php?search_type=title&value={query}"


def get_search_url(query):
    return search_url.format(query=quote_plus(query))


r = requests.get(get_search_url("all too well"))

soup = BeautifulSoup(r.text, "lxml")
result_lines = soup.findAll(attrs={"class": "tresults"})[0].findAll('tr')[1:]

artist = ""
for result_line in result_lines:
    tds = result_line.findAll('td')

    curr_artist = tds[0].text.strip()
    artist = curr_artist if curr_artist else artist

    # get and check the tab type
    tab_type = tds[-1].strong.text

    if tab_type not in ['chords', 'tab']:
        continue

    link = tds[1].findAll("a", attrs={"class": "song result-link"})[0]['href']

    print("artist: {}\nlink:{}\ntab_type: {}".format(artist, link, tab_type))
