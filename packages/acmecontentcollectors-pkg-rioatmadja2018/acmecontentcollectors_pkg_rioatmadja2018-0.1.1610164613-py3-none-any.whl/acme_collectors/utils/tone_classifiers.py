#!/usr/bin/env python
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer 
import joblib 
import os 
from acme_collectors.utils.constants import PKL_CLF, TONES 

from typing import Dict 
"""
Name: Rio Atmadja
Date: January 08,2020 
Description: tone classifier utilities 
"""

def classify_tones(text) -> Dict : 
    """
    Description 
    ------------

    Parameters
    -----------
    :text: given a non-empty text 

    Return
    ------
    :return: a dictionary with analytical, joy, sadness, fear, confident, anger, and tentative attributes 
    """ 
    if not text: 
        raise ValueError(f"You must provide a non-empty text.")

    if not os.path.exists(PKL_CLF): 
        raise FileNotFoundError(f"Unable to find the following file : {PKL_CLF}. Please check for this file. {os.getcwd()}")

    # unpack pickle classifier here 
    pkl = joblib.load(PKL_CLF)
    rf, tfidf, vect = tuple(pkl.values())

    results: Dict = dict(zip(TONES, rf.predict_proba(tfidf.transform(vect.transform([text]))).tolist()[0] )) 

    return results 