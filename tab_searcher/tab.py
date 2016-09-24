import requests
from bs4 import BeautifulSoup

example_tab_url = "https://tabs.ultimate-guitar.com/t/taylor_swift/all_too_well_crd.htm"


def get_tab_text():
    r = requests.get(example_tab_url)
    soup = BeautifulSoup(r.text, "lxml")
    tab = soup.findAll("pre", attrs={"class": "js-tab-content"})[0].text
    return tab
