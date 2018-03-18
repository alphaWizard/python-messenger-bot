import re,random
def match_rule(rules, message):
    response, phrase = "default", None
    
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

sd = input()
print(respond(sd))