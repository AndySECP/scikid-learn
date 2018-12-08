import json
import pandas as pd

import nltk
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
# from __future__ import division, print_function # make it run on py2 an d py3
import requests # The requests library is an HTTP library for getting c ontent and posting etc.
import bs4 as bs # BeautifulSoup4 is a Python library for pulling data out of HTML and XML code. We can query markup languages for specific content
import urllib.parse, urllib.request, json

from flask import Flask, render_template, json, request
from werkzeug import generate_password_hash, check_password_hash
#from flaskext.mysql import MySQL

f = open("createKey_json.txt","r")
s = f.read()
keys = json.loads(s)
keys = keys["password"]


def CallWikifier(text, threshold=-1):  # lang="en"
    print("Running wikifier")
    data = urllib.parse.urlencode([
        # Convert a mapping object or a sequence of two-element tuples to a percent-encoded ASCII text string
        ("text", text),  # text of the document to annotate; language: English ("lang", lang)
        ("userKey", keys),  # string that uniquely identifies each user
        ("wikiDataClasses", "false"),
        ("wikiDataClassIds", "false"),
        ("support", "false"),
        # for each annotation, whether to include a list of subrange in the doc that support this annotation.
        ("ranges", "false"),
        # whether to include, for each subrange in doc that looks like a possible mention of a concept, a list of all annotations for that subrange.
        ("includeCosines", "false"),  # the cosine similarity between the input document and the Wikipedia page
        ("maxMentionEntropy", "2"),
        ("maxTargetsPerMention", "2"),
        ("minLinkFrequency", "1"),
        ("pageRankSqThreshold", "%g" % threshold),
        ("applyPageRankSqThreshold", "false"),
        ("partsOfSpeech", "false"),
        ("nTopDfValuesToIgnore", "200"),  # if a phrase consists entirely of very frequent words, it will  be ignored
        ("nWordsToIgnoreFromList", "-1")])

    url = "http://www.wikifier.org/annotate-article"
    req = urllib.request.Request(url, data=data.encode("utf8"), method="POST")
    with urllib.request.urlopen(req, timeout=60) as f:
        response = f.read()
        response = json.loads(response.decode("utf8"))
    # Output
    #     with open("result.txt","w") as t:
    #         t.write(json.dumps(response))

    #     for annotation in response["annotations"]:
    #         print("%s (%s)" % (annotation["title"], annotation["url"]))


    # each pair of output in a single bracket
    #     with open("result.txt","w") as t:
    #         for annotation in response["annotations"]:
    #             resuls={annotation["title"]: annotation["url"]}
    #             results =json.dumps(result)
    #             print("%s (%s)" % (annotation["title"], annotation["url"]))
    #             #t.write("%s %s"%(annotation["title"],annotation["url"]) + '\r\n')
    #             t.write(results)

    # all pairs of output in one bracket
    results = {}
    with open("result.txt", "w") as t:
        for annotation in response["annotations"]:
            print("%s (%s)" % (annotation["title"], annotation["url"]))
            #results = {annotation["title"]: annotation["url"]}
            #result.update(results)
            results[annotation["title"]] = annotation["url"]
            # t.write("%s %s"%(annotation["title"],annotation["url"]) + '\r\n')
        #results = json.dumps(result)
        #t.write(results)
    return results
