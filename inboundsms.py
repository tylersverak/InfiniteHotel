from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
app = Flask(__name__)
from infinitehotelmain import hotelmain, add_text, add_player
import threading

# instructions- run web server for receiving texts, then run 'ngrok http 5000' cause webserver default is 5000 and then you
# gotta put ngrok url in the API

SINGLE_PLAYER = True # should we add one player using the command line?

players = {} # dictionary of existing players in a string:string pair of phone number:name

# webhook for incoming SMS
@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    body = request.values.get('Body', None)
    number = request.values.get('From', None)
    if not number in players.keys(): # if no texts have been received from this number
        players[number] = None
        resp = MessagingResponse()
        resp.message("Hello new player! What is your name?")
        return str(resp )
    elif players[number] == None: # if an intro has been sent, but player doesn't have a name yet, assign text message as player name and create Player object in the game
        players[number] = body.strip()
        add_player(players[number], number)
        resp = MessagingResponse()
        resp.message("Cool. Welcome " + players[number] + "! Hope that is your name cause I can't change it now. We'll put your character in the hotel lobby. Go ahead and text 'inspect guide' to get start playing.")
        return str(resp )
    else: # if the player exists and phone number is already recorded, send text to game
        add_text((body, number))
    return ""
    # other helpful functions
    #resp = MessagingResponse()
    #msg = resp.message("sample message from web server" + " " + str(data))
    # add image
    #msg.media( "https://farm8.staticflickr.com/7090/6941316406_80b4d6d50e_z_d.jpg")
    #return str(resp ) # directly responds


if __name__ == "__main__":
    print('start')
    if SINGLE_PLAYER:
        hotelmain(True)
    else:
        x = threading.Thread(target=hotelmain, args=()) # run the game in a seperate thread
        x.setDaemon(True)
        x.start()
        app.run(host='127.0.0.1', debug=True) # host a local webserver
    print('end')