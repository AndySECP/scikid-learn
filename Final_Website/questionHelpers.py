import numpy as np
import pandas as pd
import os
import ast

def getQuestion(qString):
    """
    Given a q string like:
    '
    'Which organism needs to make its own food? 
    (A) {Alaska-2008-4-5} 
    (B) {Alaska-2008-4-6} 
    (C) {Alaska-2008-4-7} 
    (D) {Alaska-2008-4-8}'
    '
    
    returns the question,
    
    'Which organism needs to make its own food?'
    """
    return qString.split('(')[0].strip()


def cleanAns(ans):
    """
    Takes string of answers like
    "{'(A)': '{Alaska-2008-4-5} ', 
    '(B)': '{Alaska-2008-4-6} ', 
    '(C)': '{Alaska-2008-4-7} ', 
    '(D)': '{Alaska-2008-4-8} '}"
    
    and returns a cleaned up dictionary
    "{'A': 'Alaska-2008-4-5'...}
    
    """
    import ast
    dictLike = ast.literal_eval(ans)
    out = dict()

    for k,v in dictLike.items():
        newK = k.strip('(').strip(')').strip()
        newV = v.strip().strip('{').strip("}").strip()
        out[newK] = newV
        
    return out


def hasChart(string):
    """
    Use on question strings
    to find where images, charts, etc
    have been used. 
    
    Returns boolean array
    
    used to find strings only dependent on
    language
    """
    return "{" in string


def dynamicQuestionOutput(index, data):
    """
    Given processed data (data, a dataframe)
    and a location index
    
    returns dictionary containing:
    
    1) Question: the question, a string
    2) Correct: the right answer, a string
    3) A: option A
    4) B: option B
    5) C: option C
    6) D: option D
    """
    vals = data.iloc[index]
    answers = cleanAns(vals['split answers'])
    answers['Question'] = vals['Q only']
    answers['Correct'] = vals['AnswerKey']
    return answers

def answers(dynamicQ):
    out = dict()

    out['A'] = dynamicQ['A']
    out['B'] = dynamicQ['B']
    out['C'] = dynamicQ['C']
    out['D'] = dynamicQ['D']

    return out





