#Created on Wed Nov 14 23:40:50 2018

#@author: Andy

from __future__ import division, print_function # make it run on py2 an d py3
import nltk
import pandas as pd
import bs4 as bs
from nltk.tokenize import sent_tokenize # tokenizes sentences
import re
from nltk.stem import PorterStemmer
from nltk.tag import pos_tag
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from IPython.core.display import display, HTML 
display(HTML("<style>.container { width:90% !important; }</style>")) #if 100% it would fit the screen
import requests # The requests library is an HTTP library for getting c ontent and posting etc.
import bs4 as bs # BeautifulSoup4 is a Python library for pulling data out of HTML and XML code. We can query markup languages for specific content
import urllib.parse, urllib.request, json



def CallWikifier(text, lang="en", threshold=0.7):
    data = urllib.parse.urlencode([
        ("text", text), ("lang", lang),
        ("userKey", "rearpqcxiusxybnwbmmrjnvxinkuwa"),
        ("pageRankSqThreshold", "%g" % threshold), ("applyPageRankSqThreshold", "true"),
        ("nTopDfValuesToIgnore", "0"), ("nWordsToIgnoreFromList", "-1"),
        ("wikiDataClasses", "true"), ("wikiDataClassIds", "false"),
        ("support", "false"), ("ranges", "true"),
        ("includeCosines", "false"), ("maxMentionEntropy", "3"), ("maxTargetsPerMention","6")])
    url = "http://www.wikifier.org/annotate-article"
    req = urllib.request.Request(url, data=data.encode("utf8"), method="POST")
    with urllib.request.urlopen(req, timeout = 60) as f:
        response = f.read()
        response = json.loads(response.decode("utf8"))
    # Output
    for annotation in response["annotations"]:
        print("%s (%s)" % (annotation["title"], annotation["url"]))