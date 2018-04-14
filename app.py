from flask import Flask
from datetime import datetime
import sys
import operator

# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


app = Flask(__name__)

@app.route('/')
def homepage():
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")

    return """
    <h1>Hello heroku</h1>
    <p>It is currently {time}.</p>
    <img src="http://loremflickr.com/600/400" />
    """.format(time=the_time)

@app.route('/parse', methods=['GET'])
def main():
    html = request.args['html']
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


@app.route('/testroute')
def testroute():
    return "test text"


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
