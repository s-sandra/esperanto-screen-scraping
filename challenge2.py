# @authors Sandra Shtabnaya and Matthew Karp

from bs4 import BeautifulSoup

# parses esperanto.html using html parser
soup = BeautifulSoup(open("esperanto.html", encoding="utf8"), "html.parser")