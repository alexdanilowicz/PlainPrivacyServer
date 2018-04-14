# -*- coding: utf-8 -*-

import sys
import operator

# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

def main(html):

    language_client = language.LanguageServiceClient()

    document = language.types.Document(
        content=html,
        type=language.enums.Document.Type.HTML)

    entities = language_client.analyze_entities(document).entities
    sally = {}
    for entity in entities:
        word = entity.name.lower()
        score = sally.get(word, 0)
        score += entity.salience
        sally[word] = score

    sorted_sally = sorted(sally.items(), key=operator.itemgetter(1), reverse=True)

    for word, score in sorted_sally:
        print('=' * 20)
        print(u'{:<16}: {}'.format('name', word))
        print(u'{:<16}: {}'.format('score', score))



    return sorted_sally[:3]

main()
