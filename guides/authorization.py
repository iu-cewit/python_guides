#!/usr/bin/env python

# Uses requests library: http://docs.python-requests.org/en/latest/
# import requests
import urllib
import argparse
import urlparse
import getpass
import mechanize
import requests


'''
OAuth 2.0 really needs to do three things.

1) Make a request for the OAuth Dialog form with client secret and redirect_uri
2) After client interaction redirect_uri is called with auth code or error
3) Finally auth code is exchanged for a long lived access token

To run simply

cd ROOT_OF_PACKAGE
pip install -r requirements.txt
python ./guides/authorization.py CLIENT_ID CLIENT_SECRET REDIRECT_URI API_KEY

'''

SM_API_BASE = "https://api.surveymonkey.net"
AUTH_CODE_ENDPOINT = "/oauth/authorize"
ACCESS_TOKEN_ENDPOINT = "/oauth/token"


# Parse the data from the commandline
def main():
    parser = argparse.ArgumentParser(description='Demo OAuth 2.0')

    parser.add_argument("client_id", help='Username from Mashery')
    parser.add_argument("client_secret", help='Secret from Mashery')
    parser.add_argument("redirect_uri", help='redirect uri for auth-code')
    parser.add_argument("api_key", help='API key for your app')
    args = parser.parse_args()

    # Step 1 Load oauth dialog and take user input
    redirect_uri = oauth_dialog(args.client_id, args.redirect_uri, args.api_key)
    if redirect_uri is None:
        return None
    # Step 2 Parse authorization token from redirect response
    auth_code = handle_redirect(redirect_uri)

    if auth_code:
        # Step 3 exchange your authorization code for a long lived access token
        access_token = exchange_code_for_token(auth_code, args.api_key,
                                               args.client_id, args.client_secret,
                                               args.redirect_uri)
        if access_token:
            print 'Your long lived access token is ' + access_token
            return access_token
        else:
            return None
    else:
        print 'No Authorization Code was returned. Were the username and ' \
              'password correct?'
        return None


def oauth_dialog(client_id, redirect_uri, api_key):
    # Construct the oauth_dialog_url
    url_params = urllib.urlencode({
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'response_type': 'code',
        'api_key': api_key
    })
    auth_dialog_uri = SM_API_BASE + AUTH_CODE_ENDPOINT + '?' + url_params

    print "\nThe auth dialog url was " + auth_dialog_uri + "\n"

    # Emulate redirecting user to the oauth dialog url
    browser = mechanize.Browser()
    try:
        browser.open(auth_dialog_uri)
    except:
        print 'Ran into trouble with your credentials. Are you sure your client_id, '\
              'redirect_uri, and api_key are correct?'
        return None
    # User fills in the form
    login_form = browser.forms().next()
    login_form['username'] = raw_input('SurveyMonkey Username: ')
    login_form['password'] = getpass.getpass('SurveyMonkey Password: ')
    browser.form = login_form

    # Form is submitted, browser is redirected to your callback url
    response = browser.submit()

    return response.geturl()


def handle_redirect(redirect_uri):
    # Parse authorization code out of url
    query_string = urlparse.urlsplit(redirect_uri).query
    authorization_code = urlparse.parse_qs(query_string).get('code', [])

    # parse_qs returns a list for every query param, just get the first one
    if len(authorization_code) > 0:
        return authorization_code[0]
    else:
        return None


def exchange_code_for_token(auth_code, api_key, client_id, client_secret,
                            redirect_uri):
    data = {
        "client_secret": client_secret,
        "code": auth_code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "grant_type": "authorization_code"
    }

    access_token_uri = SM_API_BASE + ACCESS_TOKEN_ENDPOINT + '?api_key=' + api_key
    access_token_response = requests.post(access_token_uri, data=data)
    access_json = access_token_response.json()

    if 'access_token' in access_json:
        return access_json['access_token']
    else:
        print 'Problems exchanging the auth code for your access token. Error messge: %s' % access_json['error_description']
        return None


# Bootstrap script to call into main
if __name__ == "__main__":
    main()
