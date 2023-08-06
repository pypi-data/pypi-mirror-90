import re

# This gets rid of most HTML w/o resorting to BeautifulSoup (which we might do at some point)
def clean_html(s):
    cleanr = re.compile('<.*?>')
    clean_text = re.sub(cleanr, '', s)
    return clean_text
