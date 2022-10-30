from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
app = Flask(__name__)
from infinitehotelmain import hotelmain, add_text, add_player
import threading
import time

# instructions- run web server for receiving texts, then run 'ngrok http 5000' cause webserver default is 5000 and then you
# gotta put ngrok url in the API

players = {}
data = []

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""

    body = request.values.get('Body', None)
    number = request.values.get('From', None)
    print(players)
    if not number in players.keys():
        players[number] = None
        resp = MessagingResponse()
        resp.message("Hello new player! What is your name?")
        return str(resp )
    elif players[number] == None:
        players[number] = body.strip()
        add_player(players[number], number)
        resp = MessagingResponse()
        resp.message("Cool. Welcome " + players[number] + "! Hope that is your name cause I can't change it now. We'll put your character in the hotel lobby. Go ahead and text 'inspect guide' to get start playing.")
        return str(resp )
    else:
        add_text((body, number))
    return ""
    # Start our TwiML response
    #resp = MessagingResponse()
    # Add a message
    #msg = resp.message("sample message from web server" + " " + str(data))

    # add image
    #msg.media( "https://farm8.staticflickr.com/7090/6941316406_80b4d6d50e_z_d.jpg")
    #return str(resp )


if __name__ == "__main__":
    print('start')
    x = threading.Thread(target=hotelmain, args=())
    x.setDaemon(True)
    x.start()
    app.run(host='127.0.0.1', debug=True)
    print('end')