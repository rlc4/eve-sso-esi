import os
from pprint import pprint
from flask import Flask, request, session, render_template, url_for, redirect
from flask_oauthlib.client import OAuth
from API import swagger_client
from API.swagger_client.rest import ApiException
import config as config

## Setting up the Flask application
app = Flask(__name__)

## These URLs are needed by the OAuthlib client, but are held in the flask app
app.config['EVESSO'] = dict(
    consumer_key=config.EVESSO_CLIENT_ID,
    consumer_secret=config.EVESSO_SECRET_KEY,
    base_url='https://login.eveonline.com/oauth/',
    access_token_url='/oauth/token',
    access_token_method='POST',
    authorize_url='/oauth/authorize',
    request_token_params={'scope': config.scopes}
)
app.secret_key = config.secret_key

# Initializes OAuth using the config we've put in the app above
oauth = OAuth()
oauth.init_app(app)
evesso = oauth.remote_app('evesso', app_key='EVESSO')

# but wait, we also need to config the swagger_client that we
# generated using setup.py
configuration = swagger_client.Configuration()


# render the initial index:
#  - before login it only shows "login"
#  - after login it shows character and token info
@app.route("/")
def index():
    return render_template("index.html")

# enact the oauth SSO flow, sends you to EVE to login with the specified scopes
@app.route("/login")
def login():
    return evesso.authorize(callback=url_for('authorized', _external=True, _scheme="http"))

# oauth redirects your browser to the callback location
@app.route('/oauth-response')
def authorized():
    resp = evesso.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    if isinstance(resp, Exception):
        return 'Access denied: error=%s' % str(resp)

    # Getting the token and stuffing it into the proper places
    # session - Flask_oauthlib - we can do GET and POST with this if we want
    session['evesso_token'] = (resp['access_token'], '')
    # and stuffing the access_token into the right place for the swagger_client
    # to be able to use it.
    configuration.access_token = resp['access_token']

    verify = evesso.get("verify")
    session['character'] = verify.data
    return redirect(url_for("index"))

# once we've gotten a callback to oauth-response, we can get tokens
# to access the API
@evesso.tokengetter
def get_evesso_oauth_token():
    return session.get('evesso_token')

# an example of using the API, we added the token up above
@app.route("/charStandings")
def standings():
    char = swagger_client.CharacterApi(swagger_client.ApiClient(configuration))
    resp = char.get_characters_character_id_standings(character_id=session['character']['CharacterID'])
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    if isinstance(resp, Exception):
        return 'Access denied: error=%s' % str(resp)
    return render_template("standings.html", standings=resp)

# and when we're done, we can log out, destroying the session (flask) and the token (swagger_client)
@app.route("/logout")
def logout():
    session.clear()
    configuration.access_tokan = ""
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True,port=config.PORT)
