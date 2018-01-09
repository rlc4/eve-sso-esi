# import random
# import string

PORT = 8888

datasource = 'tranquility'
user_agent = 'YourAppNameOrSomethingSimilar'

# hint: when you set up your application for testing, set your callback
# to: localhost:8888/oauth-callback

EVESSO_SECRET_KEY = "From your Developer page for your app"
EVESSO_CLIENT_ID = "From your Developer page for your app"

secret_key = "Something to secure your tokens: only you know this keep it safe or random"
# If you want something random each time you run your program, then use: ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])

# The scopes your application needs
scopes = ['esi-characters.read_standings.v1']
