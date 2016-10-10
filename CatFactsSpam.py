import urllib2
import json
from twilio.rest import TwilioRestClient
from flask import Flask, request, redirect
import twilio.twiml
from random import randint
import threading
import os

app = Flask(__name__)

@app.route("/spam", methods=['GET', 'POST'])
def cat_spam():

    number = request.args.get('number')

    if number.find("+1") == -1:
        number = "+1" + number

    SendInfo(number)
    SendFact(number)

    return "Spamming Target."

@app.route("/reply", methods=['GET', 'POST'])
def cat_reply():

    req = urllib2.Request("http://catfacts-api.appspot.com/api/facts?number=1")
    full_json = urllib2.urlopen(req).read()
    cat_fact = json.loads(full_json)

    random_code = randint(10000000,99999999)

    resp = twilio.twiml.Response()
    resp.sms("You've just subscribed to another 6 hours of CatFacts. Thank you for using CatFacts! To cancel please reply %s." %(random_code))
    resp.sms(cat_fact['facts'][0])
    return str(resp)

def SendInfo(number):
    account = os.environ['TWILIOACCOUNT']
    token = os.environ['TWILIOAUTH']
    client = TwilioRestClient(account, token)

    message = client.sms.messages.create(to=number, from_=os.environ['TWILIONUMBER'],
    body="You've been given 6 hours of free CatFacts! Reply 'Dogs' to stop these messages. ")

def SendFact(number):
    threading.Timer(1800, SendFact, [number]).start()  ### 1800 for 30 min, 3600 for 1 hr

    req = urllib2.Request("http://catfacts-api.appspot.com/api/facts?number=1")
    full_json = urllib2.urlopen(req).read()
    cat_fact = json.loads(full_json)

    account = os.environ['TWILIOACCOUNT']
    token = os.environ['TWILIOAUTH']
    client = TwilioRestClient(account, token)

    message = client.sms.messages.create(to=number, from_=os.environ['TWILIONUMBER'],
    body= cat_fact['facts'][0])

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
