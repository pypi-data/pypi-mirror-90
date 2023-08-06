#!/usr/bin/env python 
from acme_collectors.utils.tone_classifiers import classify_tones 
from unittest import TestCase  
from typing import Dict, List 

news_article: str = """
In a statement, United Nations Secretary-General Antonio Guterres’s spokesman urged for “restraint and the need to avoid any actions that could lead to an escalation of tensions in the region”.
But Iran’s Supreme Leader Ali Hosseini Khamenei called for the killers to be brought to justice, and a sense of discomfort has settled over some Iraqis.
The killing of one of Iran’s towering figures felt reminiscent of the assassination of top Iranian General Qassem Soleimani in January.
The killing of Soleimani by a US air strike paved the path towards an uptick in violence between American troops and Iran-backed armed groups, like Kataib Hezbollah.
The group released a statement following the killing of Fakhrizadeh calling for revenge against the “Zionist-American-Saudi axis’ criminal record. The cost of their crimes must be high.”
"""
class TestClassifier(TestCase):

    def test_classify_tone(self):

        response: Dict = classify_tones(news_article)
        print(f"[+] RESPONSE: {response} ")
        result: List[float] =  [0.66, 0.05, 0.03, 0.03, 0.1, 0.1, 0.03] 
        return self.assertListEqual(result, list(response.values()))