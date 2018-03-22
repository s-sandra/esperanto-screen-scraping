# @authors Sandra Shtabnaya and Matt Karp

from bs4 import BeautifulSoup

# parses esperanto.html using html parser
soup = BeautifulSoup(open("esperanto.html", encoding="utf8"), "html.parser")

# gets the data in the second table, containing common esperanto words
words_tds = soup.find_all("td")[10:]

for word_cols in words_tds:
    words = word_cols.find_all("li")

    for word in words:
        root = word.get_text()
        style = word.attrs # might have bold style.
        color = word.a.attrs # might be red or green. Otherwise, blue.