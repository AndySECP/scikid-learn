# SciKid-Learn
2018 - Academic project at UC Berkeley, merging both the issues of Education and Artificial Intelligence. <br /> <br />
This project was presented at the **SIGKDD2019** at Anchorage during the *Social Impact Workshop*.

## Objectives

Improve the way students learn thanks to customized recommendation of learning contents based on their test results. Providing a personnalized education tools by adapting to each student learning style thanks to unsupervised clustering algorithms. Providing insights for students and teachers as well. 

## Project Plan

* October: _Topic Understanding and Database Management_
* November: _Algorithms development and front end development_
* December: _Final product delivery_

## Team Members

* El Bouri, Niema: _niema_elbouri@berkeley.edu_
* Lawrence, Mike: _mikelawrence@berkeley.edu_
* Shan, Shine: _shine_shan@berkeley.edu_
* Tanyindawn, Ada: _adatanyindawn@berkeley.edu_
* Spezzatti, Andy: _andy_spezzatti@berkeley.edu_

## Supervisors

* Košmerlj, Aljaž: _aljaz.kosmerlj@ijs.si_
* Hodson, James: _hodson@ai4good.org_

## Concept

![concept](https://user-images.githubusercontent.com/38164557/61997436-3f77c280-b056-11e9-8d4a-fa85ccfc66ac.JPG)

## Architecture of the solution

![Architecture](https://user-images.githubusercontent.com/38164557/61997417-1b1be600-b056-11e9-9a18-57b306bf5aa0.JPG)

## Clustering of questions by academic subjects

Leveraging dimensionality reduction technique, we can get some insights into the different hierarchies of subjects present in our database

<p align="center">
  <img src="https://user-images.githubusercontent.com/38164557/62025653-a51a9a80-b18d-11e9-9f79-7704c444bbd1.JPG" width="500">
</p>
 
 With a bubble plot, we can then visualize which words are more important and reflect more accuratly one cluster. A similar analysis can be done for higher n-grams.
 
 <p align="center">
  <img src="https://user-images.githubusercontent.com/38164557/62025697-cbd8d100-b18d-11e9-8325-04530104582f.JPG" width="500">
</p>

## Customized Named Entity Recognition model

Using Spacy's ner model and fine tuned it using our own annotated examples, we created our own ner model. We first added a couple of classes, useful for our application (detecting academic subjects and cognitive skills):<br />
*PHY: physic* <br />
*BIO: biology* <br />
*VIZ: visualization* <br />
*SHAPE: shape* <br />
*CLIM: climatology* <br />
*ANM: animals* <br />
*GEO: geology* <br />
*COMP: comparison* <br />

The training of the ner model can be done by using:
```python
python ner_cust.py -m=en -o="path/to/output/directory" -n=100
```


