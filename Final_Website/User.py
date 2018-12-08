import pandas as pd
import os
import pickle

class User:

    def __init__(self, email, name, data):
        self.email = email
        self.name = name
        self.data = data
        self.recorded = dict()
        self.dataDirectory = "userData/"

        if self.returningUser():
            self.retrieveData()




    ## Storage ##
    def returningUser(self):
        return self.name in os.listdir(self.dataDirectory)

    def storeData(self):
        out = open(self.dataDirectory + self.name,'wb')
        pickle.dump(self.recorded, out)
        out.close()

    def retrieveData(self):
        file = open(self.dataDirectory + self.name,'rb')
        new_dict = pickle.load(file)
        file.close()

        self.recorded = new_dict



    ## Interface with Questions ##
    def hasSeen(self, questionID):
        return questionID in self.recorded.keys()

    def recordOutcome(self, questionID, outcome):
        self.recorded[questionID] = outcome

        if len(self.recorded.keys()) % 10 == 0:
            self.storeData()



    ## Get Performance Data for Dashboards, etc ##
    def getAllHistory(self):
        return self.recorded

    def getPerformance(self):

        qid = []
        answered = []
        correct = []
        outcome = []

        for k, v in self.recorded.items():
            assert type(k) == int
            assert type(v) == str

            qid += [k]
            answered += [v]
            correct += [self.data.iloc[k]["AnswerKey"]]
            outcome += [self.data.iloc[k]["AnswerKey"].strip().lower() == v.strip().lower()]

        qid = pd.Series(qid)
        answered = pd.Series(answered)
        correct = pd.Series(correct)

        data = {"QuestionID": qid,
                "Response": answered,
                "Correct": correct,
                "Outcome": outcome}

        data = pd.DataFrame(data)

        return data


    def htmlTable(self, head=None):
        if head != None:
            return self.joinOnOriginal().head(head).to_html(classes=["table-bordered", "table-striped", "table-hover"])

        return self.joinOnOriginal().to_html(classes=["table-bordered", "table-striped", "table-hover"]) 

    def joinOnOriginal(self):

        perf = self.getPerformance()
        keep = list(perf.columns) + ['schoolGrade', 'question', 'subject']
        joined = perf.join(self.data, on='QuestionID')[keep]

        return joined

    def getSubject(self, category):
        data = self.joinOnOriginal()
        subset = data[data['subject'] == category]
        return subset

    def subjectAccuracy(self, category):
        data = self.getSubject(category)

        count = data.shape[0]
        correct = data['Outcome'].sum()
        accuracy = data['Outcome'].mean()

        return [count, correct, accuracy]

