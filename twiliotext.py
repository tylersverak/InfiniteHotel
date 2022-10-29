import twiliosecret

from twilio.rest import Client

from twiliosecret import ACCOUNT_SID

from twiliosecret import AUTH_TOKEN

from twiliosecret import TWILIO_NUMBER

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def send_twilio_text(text, to_num = "+19255968020"):
    print('debug' + to_num)
    message = client.messages.create(
        to=to_num, 
        from_=TWILIO_NUMBER,
        body=text)
    print("Message sent to " + to_num)