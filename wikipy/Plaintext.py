# %%
import re

# %%
class Plaintext:
    def __init__(self, text):
        self.title = re.findall(r'\A(.*)From Wikipedia', text)
        self.title = self.title[0].strip().replace(' ','_')
        self.articles = re.findall(r'\|\|(\S+)\|\|', text)
        self.text = text.replace("||","")
# %%
file_name = "../CleanPages/World_War_II.txt"
text_file = open(file_name, "r")
text = text_file.read()


pt = Plaintext(text)

# %%
pt.title
# %%
pt.articles
# %%
pt.text
