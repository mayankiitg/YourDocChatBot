#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

#Global Variables
UserSymptomsData = dict()   #Stores user symptoms. Key: sessionId, Data: List of Symptoms


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    print("Result: ")
    print(res)
    r = make_response(res)
    # r = make_response("Hello")
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    print("Processing Request: sessionId" + req.get("sessionId"))
    try:    
        if req.get("result").get("action") == "add_symptom":
            print("Action: add_symptom")
            if len(req.get("result").get("parameters").get("Symptoms")) == 0:
                print("No Symptom Found")
                outStr = "Couldn't Understand the symptom. Kindly rephrase ur query."
            else:
                print("Symptoms Found")
                addSymptomInList(req)
                outStr = "Do You have any other symptom"

        elif req.get("result").get("action") == "predict_disease":
            print("Action: predict_disease")
            outStr = predictDisease(req)
        
        else:
            print("No action Detected")
            return {}
        
        res = makeWebhookResult(outStr)
        return res
    except Exception as e:
        print("Error in Process Request. + " + e)
        return {}

def addSymptomInList(req):
    try:
        symptoms = req.get("result").get("parameters").get("Symptoms")    #List of string
        sessionId = req.get("sessionId")                #String
        if sessionId in UserSymptomsData:
            UserSymptomsData[sessionId] += symptoms
        else:
            UserSymptomsData[sessionId] = symptoms
        print("Added following symptom: in session " + str(sessionId) + " ".join(symptoms))
    except Exception as e:
        print("Error in Process Request. + " + e)

def predictDisease(req):
    sessionId = req.get("sessionId")                #String
    return "Symptoms are " + (", ".join(UserSymptomsData[sessionId]))

def makeWebhookResult(outStr):
    print("Response:")
    print(outStr)

    return {
        "speech": outStr,
        "displayText": outStr,
        # "data": data,
        # "contextOut": [],
        "source": "yourdoc"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
