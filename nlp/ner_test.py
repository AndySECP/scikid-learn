from __future__ import unicode_literals, print_function
import pickle
import plac
import random
from pathlib import Path
import spacy
from spacy.util import minibatch, compounding

test_text = "".join(["Use the information below to answer the question Several students placed a toy truck on a table in front of a plane",
     "mirror and viewed the image of the truck in the mirror Next the students moved the toy truck to different positions",
     "and observed the reflected images of the truck from each position How does the size of the image of the toy truck",
     "compare to the size of the actual toy truck the image is larger than the actual truck the image is smaller than the",
     "actual truck the image is the same size as the actual truck the image size depends on the light behind the toy truck"])


def test(output_dir="output", test_text=test_text):	
	print("Loading from", output_dir)
	nlp2 = spacy.load(output_dir)
	doc2 = nlp2(test_text)
	print(doc2)
	for ent in doc2.ents:
		print(ent.label_, ent.text)


if __name__ == '__main__':
	test()
