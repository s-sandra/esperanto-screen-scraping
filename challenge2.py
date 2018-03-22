# @authors Sandra Shtabnaya and Matt Karp

from bs4 import BeautifulSoup

# parses esperanto.html using html parser
soup = BeautifulSoup(open("esperanto.html", encoding="utf8"), "html.parser")

# gets the data in the second table, containing common esperanto words
word_data = soup.find_all("td")[10:]

for word_cols in word_data:
    for word in word_cols.ol:
        print("one thing: ", word)