# @authors Sandra Shtabnaya and Matt Karp

from bs4 import BeautifulSoup
import pandas as pd

# parses esperanto.html using html parser
soup = BeautifulSoup(open("esperanto.html", encoding="utf8"), "html.parser")

# gets the data containing common esperanto words
words_tds = soup.find_all("td")[10:]

rows = []

# gets all the words in each ordered list.
for word_cols in words_tds:
    words = word_cols.find_all("li")
    common = False
    pos = "misc" # the default part of speech is misc.

    for word in words:
        root = word.get_text()
        style = word.attrs # might have bold style, indicating a common word.
        color = word.a.attrs # might be red or green. Otherwise, blue.

        root = root.strip("\n") # removes new line characters

        # checks if the word has a font-weight style
        if style:
            if "bold" in style["style"]:
                common = True

        # checks if the word has a color style
        if "style" in color:
            color = color["style"]

            if "255" in color: # red has r value of 255.

                # only an intransitive verb if root ends with "i".
                pos = "VI"

            if "51" in color: # blue has g value of 204

                # only a transitive/intransitive verb if root ends with "i"
                pos = "VTI"

        rows.append({"root" : root, "pos" : pos, "common" : common})

esperanto = pd.DataFrame(rows)
print(esperanto)