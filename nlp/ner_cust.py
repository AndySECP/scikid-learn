from __future__ import unicode_literals, print_function
import pickle
import plac
import random
from pathlib import Path
import spacy
from spacy.util import minibatch, compounding


TRAIN_DATA = [
	#BIO is an entity corresponding to biological stuff
    ("Which organism needs to make its own food", {"entities": [(6, 13, "BIO"), (37, 40, "BIO")]}),

    (("Students planted one hundred flower seeds They observed the growth of their plants once a week Which tool could be"
    	"used to record their observations"), {"entities": [(17, 27, "CARDINAL"), (29, 34, "BIO"), (36, 40, "BIO"), (76, 81, "BIO"), 
    	(83, 86, "ORDINAL"), (90, 93, "DATE")]}),

    (("Study the data table below Two students want to know how temperature affects rubber bands They decide to test rubber"
     "bands inside and outside their school during the winter The students plan to stretch each rubber band until it breaks"
      "Which set of materials should be used for this test set 1 set 2 set 3 set 4"),
      {"entities": [(10, 19, "QUANTITY"), (57, 67, "PHY"), (166, 171, "DATE"), (247, 255, "PHY"),
      (286, 290, "CARDINAL"), (292, 296, "CARDINAL"), (298, 303, "CARDINAL"), (305, 309, "CARDINAL")]}),

    ("The chart shows observations of the Moon Which drawing shows how the Moon would most likely appear on day 13", 
    	{"entities": [(4, 8, "VIZ"), (36, 39, "LOC"), (47, 53, "VIZ"), (69, 72, "LOC"), (102, 197, "DATE")]}),

    (("A balloon has a negative charge A glass rod has a positive charge What will happen when the glass rod is brought",
     "near the balloon The balloon will be attracted to the rod The balloon will be repelled by the rod The balloon will",
      "remain in place The balloon will spin in circles"), 
      {"entities": [(2, 8, "SHAPE"), (16, 32, "PHY"), (50, 64, "PHY"), (121, 127, "SHAPE"), (133, 139, "SHAPE"),
      (174, 180, "SHAPE"), (214, 220, "SHAPE"), (246, 252, "SHAPE"), (259, 262, "PHY"), (267, 273, "SHAPE")]}),

    (("The diagram below shows a landscape Where in the diagram would the air pressure be the greatest at the beach on top",
     "of the mountain at the bottom of the clouds above Earth’s atmosphere"), {"entities": [(7, 13, "LOC"), 
    	(4, 10, "VIZ"), (26, 34, "VIZ"), (49, 55, "VIZ"), (67, 78, "PHY"), (122, 129, "LOC"), (152, 157, "LOC"),
    	(165, 182, "CLIM")]}),

    (("The picture below shows several different birds What characteristic do all birds share They can fly They have feathers",
     "They have webbed feet They eat worms"), 
     {"entities": [(4, 10, "VIZ"), (42, 46, "ANM"), (75, 79, "ANM"), (110, 117, "ANM"), (149, 153, "ANM")]}),

    (("Roger collected four rock samples and wrote a description of how each was formed Which of the following rocks that",
     "Roger collected is a metamorphic rock"), {"entities": [(0, 4, "PERSON"), (16, 19, "CARDINAL"), (21, 24, "GEO"), 
    	(104, 108, "GEO"), (144, 148, "PERSON"), (165, 180, "GEO")]}),

    ("Fossils are the evidence of organisms that lived long ago Which of these animals would most likely form a fossil", 
    	{"entities": [(0, 6, "GEO"), (28, 36, "BIO"), (72, 78, "ANM"), (105, 110, "BIO")]}),

    (("Use the information below to answer the question Several students placed a toy truck on a table in front of a plane",
     "mirror and viewed the image of the truck in the mirror Next the students moved the toy truck to different positions",
     "and observed the reflected images of the truck from each position How does the size of the image of the toy truck",
     "compare to the size of the actual toy truck the image is larger than the actual truck the image is smaller than the",
     "actual truck the image is the same size as the actual truck the image size depends on the light behind the toy truck"), 
     {"entities": [(112, 116, "PRODUCT"), (139, 143, "VIZ"), (250, 265, "VIZ"), (312, 315, "COMP"), (324, 328, "VIZ"),
    	(346, 352, "COMP"), (361, 364, "COMP"), (394, 398, "VIZ"), (403, 413, "COMP"), (436, 440, "VIZ"), (445, 456, "COMP"),
    	(478, 482, "VIZ"), (491, 502, "COMP"), (528, 537, "COMP"), (554, 558, "VIZ")]}),

    (("Two circuits are shown below The light bulb of Circuit 1 does not glow The light bulb of Circuit 2 glows Which statement",
     "best explains why the light bulb of Circuit 1 does not glow Circuit 1 is an open circuit Circuit 1 is a closed circuit",
     "The positive terminal of Circuit 1 is connected to the battery"),
      {"entities": [(0, 2, "CARDINAL"), (4, 11, "PHY"), (33, 42, "PHY"), (47, 55, "PHY"), (75, 84, "PHY"), (89, 97, "PHY"),
      (142, 151, "PHY"), (156, 164, "PHY"), (180, 188, "PHY"), (201, 207, "PHY"), (209, 217, "PHY"), (224, 237, "PHY"),
      (242, 258, "PHY"), (263, 271, "PHY"), (293, 299, "PHY")]}),

    ("Some organisms require little water to live Which organism is least likely affected by a drought", 
    	{"entities": [(0, 3, "COMP"), (5, 13, "BIO"), (23, 28, "COMP"), (30, 34, "BIO"), (39, 42, "BIO"), (50, 57, "BIO"),
    	(62, 73, "COMP"), (89, 95, "CLIM")]}),
    

    (("A group of students investigated natural resources and the",
    "products humans make from these natural resources The students recorded their findings in the table below Humans do not",
    "use cows for milk for meat to make paper to make leather"), 
    {"entities": [(0, 6, "CARDINAL"), (33, 49, "BIO"), (90, 106, "BIO"), (181, 184, "ANM"), (190, 193, "ANM"), (199, 202, "ANM"),
    (225, 231, "ANM")]}),

    (("The maps below show information about the air quality for one day in June",
     "as reported from different air quality stations Which of these activities is the most likely source of poor air quality",
     "grazing cattle planting crops burning tires recycling aluminum"), 
     {"entities": [(4, 7, "GEO"), (42, 52, "CLIM"), (58, 72, "DATE"), (104, 123, "CLIM"), (153, 167, "COMP"),
     (179, 194, "CLIM")]}),
]


'''
PHY: physic
BIO: biology
VIZ: visualization
SHAPE: shape
CLIM: climatology
ANM: animals
GEO: geology
COMP: comparison
'''


LABEL = ["PHY", "BIO", "VIZ", "SHAPE", "CLIM", "ANM", "GEO", "COMP"]

@plac.annotations(
    model=("Model name. Defaults to blank 'en' model.", "option", "m", str),
    new_model_name=("New model name for model meta.", "option", "nm", str),
    output_dir=("Optional output directory", "option", "o", Path),
    n_iter=("Number of training iterations", "option", "n", int))


def main(model=None, new_model_name='new_model', output_dir="output", n_iter=10):

	print("starting")

	if model is not None:
	    nlp = spacy.load(model)  # load existing spacy model
	    print("Loaded model '%s'" % model)
	else:
	    nlp = spacy.blank('en')  # create blank Language class
	    print("Created blank 'en' model")

	if 'ner' not in nlp.pipe_names:
		ner = nlp.create_pipe('ner')
		nlp.add_pipe(ner)
	else:
		ner = nlp.get_pipe('ner')

	for i in LABEL:
	    ner.add_label(i)
	# Inititalizing optimizer
	if model is None:
	    optimizer = nlp.begin_training()
	else:
	    optimizer = nlp.entity.create_optimizer()

	other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
	with nlp.disable_pipes(*other_pipes):  # only train NER
	    for itn in range(n_iter):
	        random.shuffle(TRAIN_DATA)
	        losses = {}
	        batches = minibatch(TRAIN_DATA, 
	                            size=compounding(4., 32., 1.001))
	        for batch in batches:
	            texts, annotations = zip(*batch) 
	            # Updating the weights
	            nlp.update(texts, annotations, sgd=optimizer, 
	                       drop=0.35, losses=losses)
	        print('Losses', losses)

	# Save model 
	
	output_dir = Path(output_dir)
	if not output_dir.exists():
	    output_dir.mkdir()
	nlp.meta['name'] = new_model_name  # rename model
	nlp.to_disk(output_dir)
	print("Saved model to", output_dir)


if __name__ == '__main__':
    plac.call(main)
