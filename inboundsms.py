from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import twiliotext
app = Flask(__name__)


@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Start our TwiML response
    resp = MessagingResponse()

    # Add a message
    resp.message("The Robots are coming! Head for the hills!")
    twiliotext.send_twilio_text('sample')
    return str(resp)

def host():
    app.run(host='127.0.0.1', debug=True)
    
if __name__ == "__main__":
    print('start')
    
    print('end')