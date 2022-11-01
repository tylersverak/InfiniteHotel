import twiliosecret

from twilio.rest import Client

from twiliosecret import ACCOUNT_SID

from twiliosecret import AUTH_TOKEN

from twiliosecret import TWILIO_NUMBER

client = Client(ACCOUNT_SID, AUTH_TOKEN)

# given a message and a phone number as strings, sends text message
def send_twilio_text(text, to_num = "your number here"):
    print('debug' + to_num)
    message = client.messages.create(
        to=to_num, 
        from_=TWILIO_NUMBER,
        body=text)
    print("Message sent to " + to_num)