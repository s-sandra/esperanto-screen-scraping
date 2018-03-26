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
        pos = "misc" # the default part of speech is misc.
        root = word.get_text()
        root = root.rstrip().strip() # removes trailing and leading whitespace and newline characters.

        if root.endswith("o"):
            pos = "N" # noun

        if root.endswith("a"):
            pos = "A" # adjective

        if root.endswith("-"):
            pos = "pre" # prefix

        if root.startswith("-"):
            pos = "suf" # suffix

        common = False
        li_attrs = word.attrs # might have bold style, indicating a common word.
        bold_style = word.select("[style*=bold]") # tags underneath <li> might have bold style.

        # checks if the word has a bold font-weight style.
        if "style" in li_attrs: # if the <li> tag has a bold style attribute.
            if "bold" in li_attrs["style"]:
                common = True
        elif bold_style: # if a tag underneath <li> has a bold style attribute.
            common = True

        color_style = word.select("a[style*=color]") # <a> might have red or green color style.

        if root.endswith("i") and pos != "suf":

            # checks if the word has a color style.
            if color_style:

                # removes whitespace and newline characters within style attribute.
                color_style = color_style[0]["style"].replace("\n","").replace(" ", "")

                if "rgb(255,0,0)" in color_style: # red has rgb value of 255,0,0.
                    pos = "VI" # only an intransitive verb if red.

                elif "rgb(51,204,0)" in color_style: # green has rgb value of 51,204.,0
                    pos = "VTI"  # only a transitive/intransitive verb if green.

            else: # otherwise, the word must be blue and a transitive verb.
                pos = "VT"

        rows.append({"root" : root, "pos" : pos, "common" : common})

esperanto = pd.DataFrame(rows)[["root","pos", "common"]]
esperanto = esperanto.set_index("root") # sets the index to root.

# fumo is green, but it ends with an "o". -i starts with a hyphen, but it's blue and ends with an i.