# -*- coding: utf-8 -*-

import sys
import operator

# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

def buildKeywords():
    keywords = set()
    with open('keywords.txt') as fp:
        for line in fp:
            keywords.add(line.strip().lower())
    return keywords

def buildActions():
    actions = set()
    with open('actionable_keywords.txt') as fp:
        for line in fp:
            actions.add(line.strip().lower())
    return actions

def findOccurences(docText, keywords, actions):
    wordToList = {}
    index = 0
    for word in docText.split():
        if word in keywords or word in actions:
            occurs = wordToList.get(word,[])
            occurs.append(index)
            wordToList[word] = occurs
        index = index + 1
    return wordToList

def findMatches(wordToList):
    print('test')

def backAndForth(docText, keywords, actions, tolerance, sally):
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
                    weight = sally.get(check, 0)
                    score = score + ((1/dist) * weight)
                elif check + 's' in keywords:
                    print(word + ':' + check + 's')
                    dist = abs(index-spot)
                    weight = sally.get(check, 0)
                    score = score + ((1/dist) * weight)
                spot = spot + 1
        index = index + 1
    return score

def find_sally(text, keywords):
    keywords = buildKeywords()
    language_client = language.LanguageServiceClient()

    document = language.types.Document(
        content=text,
        type=language.enums.Document.Type.PLAIN_TEXT)

    entities = language_client.analyze_entities(document).entities
    sally = {}
    for entity in entities:
        word = entity.name.lower()
        if word in keywords or word + 's' in keywords:
            score = sally.get(word, 0)
            score += entity.salience
            sally[word] = score

    return sally


def main():
    tolerance = 12
    actions = buildActions()
    keywords = buildKeywords()
    text = open('google.txt', 'r').read()
    sally = find_sally(text, keywords)
    score = backAndForth(text, keywords, actions, tolerance, sally)
    print(score)
    return score

main()
