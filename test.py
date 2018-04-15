# -*- coding: utf-8 -*-

import sys
import operator

# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

def buildSet():
    keywords = set()
    with open('keywords.txt') as fp:
        for line in fp:
            keywords.add(line.strip().lower())
    return keywords

def main():
    keywords = buildSet()
    f = open(sys.argv[1],"r")
    text = f.read()
    language_client = language.LanguageServiceClient()

    document = language.types.Document(
        content=text,
        type=language.enums.Document.Type.HTML)

    entities = language_client.analyze_entities(document).entities
    sally = {}
    for entity in entities:
        word = entity.name.lower()
        if word in keywords or word + 's' in keywords:
            score = sally.get(word, 0)
            score += entity.salience
            sally[word] = score

    sorted_keywords = sorted(sally.items(), key=operator.itemgetter(1), reverse=True)

    for word, score in sorted_keywords:
        print('=' * 20+'\n')
        print(u'{:<16}: {}'.format('#n', word)+'\n')
        print(u'{:<16}: {}'.format('#s', score)+'\n')

    f.close()

    return sorted_keywords

main()
