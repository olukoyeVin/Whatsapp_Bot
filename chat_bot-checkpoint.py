import datetime
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

reminders = {}

@app.route('/webhook', methods=['POST'])
def webhook():
    incoming_message = request.values.get('Body', '').lower()
    response = generate_response(incoming_message)
    twilio_response = MessagingResponse()
    twilio_response.message(response)
    return str(twilio_response)

def generate_response(message):
    if message == 'hello':
        return 'Hi there! How can I assist you?'
    elif message == 'help':
        return 'I\'m here to help. What do you need assistance with?'
    elif message.startswith('remind me'):
        reminder = extract_reminder(message)
        if reminder:
            set_reminder(reminder)
            return 'Reminder set for {}'.format(reminder)
        else:
            return 'Invalid reminder format. Please use "remind me [task] on [date]"'
    else:
        return 'Sorry, I didn\'t understand your request.'

def extract_reminder(message):
    split_message = message.split('on')
    if len(split_message) == 2:
        task = split_message[0][10:].strip()
        date = split_message[1].strip()
        return {'task': task, 'date': date}
    else:
        return None

def set_reminder(reminder):
    task = reminder['task']
    date = reminder['date']
    reminder_date = datetime.datetime.strptime(date, '%Y-%m-%d')
    reminders[task] = reminder_date
##running the flask app
if __name__ == '__main__':
    app.run().
