# function that reads url from javascript
# return hmtml string

import urllib.request

def readUrl(urlString):
    print (urlString)

    urlFile = urllib.request.urlopen(urlString)
    bytesHtml = urlFile.read()
    htmlString = bytesHtml.decode("utf8")

    return htmlString

readUrl("https://www.yelp.com/tos/privacy_policy")
print("-------------------")
readUrl("https://www.airbnb.com/terms/privacy_policy")
