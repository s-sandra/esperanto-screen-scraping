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

    for word in words:
        common = False
        pos = "misc" # the default part of speech is misc.

        root = word.get_text()
        style = word.attrs # might have bold style, indicating a common word.
        color = word.a.attrs # <a> tag sometimes contains red or green color styles. Otherwise, blue.

        root = root.rstrip().strip() # removes new line characters and trailing and leading whitespace.

        if root.endswith("o"):
            pos = "N" # noun

        if root.endswith("a"):
            pos = "A" # adjective

        if root.endswith("-"):
            pos = "pre" # prefix

        if root.startswith("-"):
            pos = "suf" # suffix

        # checks if the word has a font-weight style somewhere.
        if style: # if the <li> tag has a style attribute.
            if "bold" in style["style"]:
                common = True

        elif word.span: # if the <li> element contains a span tag with a style attribute.
            if "bold" in word.span.attrs["style"]:
                common = True

        elif "style" in color: # if <a> tag under <li> has a bold font-weight attribute.
            if "bold" in color["style"]:
                common = True

        if root.endswith("i") and pos != "suf":

            # checks if the word has a color style.
            if "style" in color:
                color = color["style"]

                if "255" in color: # red has r value of 255.

                    # only an intransitive verb if root ends with "i".
                    pos = "VI"

                elif "51" in color: # green has g value of 204.

                    # only a transitive/intransitive verb if root ends with "i."
                    pos = "VTI"

            else: # otherwise, the word must be blue and a transitive verb.
                 pos = "VT"

        rows.append({"root" : root, "pos" : pos, "common" : common})

esperanto = pd.DataFrame(rows)[["root","pos", "common"]]
esperanto = esperanto.set_index("root") # sets the index to root.
esperanto.to_csv("./esperanto.csv", encoding="utf8")

# fumo is green, but it ends with an "o". -i starts with a hyphen, but it's blue and ends with an i.