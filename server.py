from flask import Flask, request
import re,random
app = Flask(__name__)

FB_API_URL = 'https://graph.facebook.com/v2.6/me/messages'
VERIFY_TOKEN = ''# <paste your verify token here>
PAGE_ACCESS_TOKEN = ''# paste your page access token here>"



def match_rule(rules, message):
    response, phrase = "sorry,what do u mean?", None
    
    # Iterate over the rules dictionary
    for pattern, responses in rules.items():
        # Create a match object
        match = re.search(pattern, message)
        if match is not None:
            # Choose a random response
            response = random.choice(responses)
            if '{0}' in response:
                phrase = match.group(1)
    # Return the response and phrase
    return response, phrase



# Define replace_pronouns()
def replace_pronouns(message):

    message = message.lower()
    if 'me' in message:
        # Replace 'me' with 'you'
        return re.sub('me', 'you', message)
    if 'my' in message:
        # Replace 'my' with 'your'
        return re.sub('my', 'your', message)
    if 'your' in message:
        # Replace 'your' with 'my'
        return re.sub('your', 'my', message)
    if 'you' in message:
        # Replace 'you' with 'me'
        return re.sub('you', 'me', message)

    return message


def respond(message):
    # Call match_rule
    rules = { 'I want (.*)': ['What would it mean if you got {0}','Why do you want {0}',"What's stopping you from getting {0}"],'do you remember (.*)': ['Did you think I would forget {0}',"Why haven't you been able to forget {0}",'What about {0}','Yes .. and?'],'do you think (.*)': ['if {0}? Absolutely.', 'No chance'],'if (.*)': ["Do you really think it's likely that {0}",'Do you wish that {0}','What do you think about {0}','Really--if {0}'] }
    response, phrase = match_rule(rules, message)
    if '{0}' in response:
        # Replace the pronouns in the phrase
        phrase = replace_pronouns(phrase)
        # Include the phrase in the response
        response = response.format(phrase)
    return response


def get_bot_response(message):
    #print(rules["I want (.*)"])
    """This is just a dummy function, returning a variation of what
    the user said. Replace this function with one connected to chatbot."""
    # response, phrase = match_rule(rules, message)
    # if '{0}' in response:
    #     # Replace the pronouns in the phrase
    #     phrase = replace_pronouns(phrase)
    #     # Include the phrase in the response
    #     response = response.format(phrase)
    # return response
    if "monday" in message:
        return "flat + soft. + algo." 
    elif "tuesday" in message:
        return "architecture + flat + soft." 
    elif "wednesday" in message:
        return "hss + architecture + flat" 
    elif "thrusday" in message:
        return "algo. + hss + architecture" 
    elif "friday" in message:
        return "off + algo + hss" 
    elif "saturday" in message:
        return "chill bro!!" 
    elif "sunday" in message:
        return "chill bro!!"                 
    else:
        rules = { 'I want (.*)': ['What would it mean if you got {0}','Why do you want {0}',"What's stopping you from getting {0}"],'do you remember (.*)': ['Did you think I would forget {0}',"Why haven't you been able to forget {0}",'What about {0}','Yes .. and?'],'do you think (.*)': ['if {0}? Absolutely.', 'No chance'],'if (.*)': ["Do you really think it's likely that {0}",'Do you wish that {0}','What do you think about {0}','Really--if {0}'] }
        response, phrase = match_rule(rules, message)
        if '{0}' in response:
            # Replace the pronouns in the phrase
            phrase = replace_pronouns(phrase)
            # Include the phrase in the response
            response = response.format(phrase)
        return response


# def get_bot_response(message):
#     """This is just a dummy function, returning a variation of what
#     the user said. Replace this function with one connected to chatbot."""
#     return "This is a dummy response to '{}'".format(message)



def verify_webhook(req):
    if req.args.get("hub.verify_token") == VERIFY_TOKEN:
        return req.args.get("hub.challenge")
    else:
        return "incorrect"

def respond(sender, message):
    """Formulate a response to the user and
    pass it on to a function that sends it."""
    response = get_bot_response(message)
    send_message(sender, response)


def is_user_message(message):
    """Check if the message is a message from the user"""
    return (message.get('message') and
            message['message'].get('text') and
            not message['message'].get("is_echo"))


@app.route('/webhook', methods=['GET', 'POST'])
def listen():
    """This is the main function flask uses to 
    listen at the `/webhook` endpoint"""
    if request.method == 'GET':
        return verify_webhook(request)

    if request.method == 'POST':
        payload = request.json
        event = payload['entry'][0]['messaging']
        for x in event:
            if is_user_message(x):
                text = x['message']['text']
                sender_id = x['sender']['id']
                respond(sender_id, text)

        return "ok"



import requests

def send_message(recipient_id, text):
    """Send a response to Facebook"""
    payload = {
        'message': {
            'text': text
        },
        'recipient': {
            'id': recipient_id
        },
        'notification_type': 'regular'
    }

    auth = {
        'access_token': PAGE_ACCESS_TOKEN
    }

    response = requests.post(
        FB_API_URL,
        params=auth,
        json=payload
    )

    return response.json()



if __name__ == '__main__':
    app.run()


