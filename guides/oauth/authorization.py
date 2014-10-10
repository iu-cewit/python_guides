#!/usr/bin/env python

import urllib
import argparse
import webbrowser
import requests
import BaseHTTPServer
from urlparse import urlparse, parse_qs

SM_API_BASE = "https://api.surveymonkey.net"
AUTH_CODE_ENDPOINT = "/oauth/authorize"
ACCESS_TOKEN_ENDPOINT = "/oauth/token"
REDIRECT_URI = "http://127.0.0.1:8000"
HOST_NAME = '127.0.0.1'
PORT_NUMBER = 8000

api_key = None
client_id = None
client_secret = None


def oauth_dialog(client_id, redirect_uri, api_key):
    """ Construct the oauth_dialog_url.
    """
    url_params = urllib.urlencode({
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'response_type': 'code',
        'api_key': api_key})

    auth_dialog_url = SM_API_BASE + AUTH_CODE_ENDPOINT + '?' + url_params
    print "\nThe auth dialog url was " + auth_dialog_url + "\n"
    webbrowser.open(auth_dialog_url, new=2)


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """ A Basic Class to handle requests to and from SurveyMonkey.
    """

    def do_HEAD(s):
        """ Sends headers.
        """
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

    def print_message(s, message):
        """ Prints a response.
        """
        s.wfile.write("<body><p>%s</p>" % message)

    def do_GET(s):
        """ Processes a response from SurveyMonkey.
        """
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write("<html><head><title>SurveyMonkey API - "
                      "OAuth Sample Redirect Page.</title></head>")

        # Parse authorization token from redirect response
        authorization_code = parse_qs(urlparse(s.path).query).get('code', [])

        # parse_qs returns a list for every query param, just get the first one
        if len(authorization_code) > 0:
            authorization_code = authorization_code[0]
        else:
            authorization_code = None

        if authorization_code:
            # Exchange your authorization code for a long lived access token
            access_token = s.exchange_code_for_token(authorization_code,
                                                     api_key, client_id,
                                                     client_secret,
                                                     REDIRECT_URI)
            if access_token:
                s.print_message('Your long lived access token is ' +
                                access_token)
            else:
                s.print_message('Error getting authorization code')

        else:
            s.print_message('No Authorization Code was returned. '
                            'Were the username and password correct?')

        s.wfile.write("</body></html>")

    def exchange_code_for_token(s, auth_code, api_key,
                                client_id, client_secret, redirect_uri):
        """ This exhanges a short term token for a long-term token.
        """
        data = {
            "client_secret": client_secret,
            "code": auth_code,
            "redirect_uri": redirect_uri,
            "client_id": client_id,
            "grant_type": "authorization_code"}

        access_token_uri = (SM_API_BASE + ACCESS_TOKEN_ENDPOINT
                            + '?api_key=' + api_key)
        access_token_response = requests.post(access_token_uri, data=data)
        access_json = access_token_response.json()

        if 'access_token' in access_json:
            return access_json['access_token']
        else:
            s.print_message('Problems exchanging the auth code for your access'
                            ' token. Error message: %s'
                            % access_json['error_description'])
            return None

# Bootstrap script to call into main
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Demo OAuth 2.0')

    parser.add_argument("client_id", help='Username from Mashery')
    parser.add_argument("client_secret", help='Secret from Mashery')
    parser.add_argument("api_key", help='API key for your app')
    args = parser.parse_args()

    client_id = args.client_id
    client_secret = args.client_secret
    api_key = args.api_key

    # Load oauth dialog and take user input
    oauth_dialog(args.client_id, REDIRECT_URI, api_key)
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    httpd.handle_request()
