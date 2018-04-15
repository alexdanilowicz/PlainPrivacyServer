#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 00:23:24 2018

@author: DylanHong
"""

from gensim.summarization import summarize

# =============================================================================
# text = "Thomas A. Anderson is a man living two lives. By day he is an " + \
#     "average computer programmer and by night a hacker known as " + \
#     "Neo. Neo has always questioned his reality, but the truth is " + \
#     "far beyond his imagination. Neo finds himself targeted by the " + \
#     "police when he is contacted by Morpheus, a legendary computer " + \
#     "hacker branded a terrorist by the government. Morpheus awakens " + \
#     "Neo to the real world, a ravaged wasteland where most of " + \
#     "humanity have been captured by a race of machines that live " + \
#     "off of the humans' body heat and electrochemical energy and " + \
#     "who imprison their minds within an artificial reality known as " + \
#     "the Matrix. As a rebel against the machines, Neo must return to " + \
#     "the Matrix and confront the agents: super-powerful computer " + \
#     "programs devoted to snuffing out Neo and the entire human " + \
#     "rebellion. "
# 
# print('Input text:')
# print(text)
# print('Summary:')
# print(summarize(text))
# =============================================================================

import sys
import operator

# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

def buildKeywords():
    keywords = set()
    with open('WhyKeywords.txt') as fp:
        for line in fp:
            keywords.add(line.strip().lower())
    return keywords

def findOccurences(docText, keywords):
    wordToList = {}
    index = 0
    print(keywords)
    for word in docText.split():
        #print(word)
        if word.lower() in keywords:
            print(word)
            occurs = wordToList.get(word,[])
            occurs.append(index)
            wordToList[word] = occurs
        index = index + 1
    return wordToList

def findMatches(wordToList):
    print('test')

def newBackAndForth(docText, keywords, actions, tolerance):
    score = 0
    index = 0
    allWords = docText.split()

    for word in allWords:
        if word in actions:
            back = max(0, index - tolerance)
            front = min(len(allWords) - 1, index + tolerance)
            spot = back
            while spot <= front:
                check = allWords[spot]
                if check in keywords:
                    print(word + ':' + check)
                    dist = abs(index-spot)
                    score = score + ((1/dist))
                elif check + 's' in keywords:
                    print(word + ':' + check + 's')
                    dist = abs(index-spot)
                    score = score + ((1/dist))
                spot = spot + 1
        index = index + 1
    return score


def findPhrase(docText,keywords):
    part = int(len(docText)/5)
    docText = docText[part:]
    noHeaderText = docText.lower()
    whyList = []
    for key in keywords:
        key = key.strip("\n")
        if noHeaderText.find(key) != -1:
            print(key)
            position = noHeaderText.index(key)
            splitList = (docText[position-1:]).split(".")
            finalString = ""
            for sentence in splitList[:7]:
                #print(sentence)
                finalString = finalString + sentence + "."
            
            whyList.append(summarize(finalString))
    
    finalString = ""
    for sentence in whyList:
        finalString = finalString + sentence + " "
    
    if finalString == "":
        finalString = "There is no summary for this privacy policy."

    print(finalString)
    return finalString

    
def main():
    forwardlook = 60
    keywords = buildKeywords()
    text = open('Hello.txt', 'r').read()
    #score = backAndForth(text, keywords, actions, forwardlook)
    #mydict = findOccurences(text,keywords)
    #print(mydict)
    findPhrase(text, keywords)
    #return score

main()
