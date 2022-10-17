import secrets

from twilio.rest import Client

from secrets import ACCOUNT_SID

from secrets import AUTH_TOKEN

from secrets import TWILIO_NUMBER

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def send_text(text, to_num = "+19255968020"):
    message = client.messages.create(
        to=to_num, 
        from_=TWILIO_NUMBER,
        body=text)
    print("Message sent to " + to_num)