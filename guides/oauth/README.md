# Note: CEWIT access token obtained directly through API console

# SurveyMonkey OAuth 2.0 Guide

## OAuth 2.0

The purpose of this guide is to walk someone through the OAuth 2.0 flow.
OAuth is an open authorization framework for web applications as defined in the
following [spec](http://oauth.net/2/).

It is used for many well-known web APIs including Google, Facebook, Amazon, Microsoft, and PayPal.
SurveyMonkey has chosen to use OAuth 2.0 as if offers good security, interoperability, and it is generally a well-understood protocol.

## Basic Idea

The basic idea is that once you register with SurveyMonkey, you can request a short term access token with your credentials.
This has an expiration of 5 minutes, so if you only plan on accessing something once, you can use this to get the desired information.
However, this short term token can be exchanged for a long term token which can be used to make repeated requests.
Currently, the long term token has no expiration on it, although this will likely change in the future.

## Setting up your credentials

A full guide for SurveyMonkey OAuth can be found [here](https://developer.surveymonkey.com/mashery/guide_oauth), so for brevity's sake, here's the abridged version.

In order to make OAuth requests, you need to first have a client identity and client secret.
These can be obtained by registering on the Surveymonkey developer network
[here](https://developer.surveymonkey.com/).

The API console has SurveyMonkey's OAuth built into it and will facilitate you obtaining an access token which will be used by your application to gain access a single (your) SurveyMonkey account. To obtain the necessary access token, choose "Custom Application" in the "Application:" dropdown, enter your API key, client ID (API user name), and client secret. Then click on the "Get Access Token" button. If you aren't already logged into SurveyMonkey, you will be prompted to enter your user name and password. If you are logged in, you will just see an "Authorize" button. Once authorized, the API console will be populated with an access token which can be used in combination with your API credentials to access to your SurveyMonkey account.

## Running

In order to run the OAuth example application, simply run the following commands:

    > cd ROOT
    > pip install -r requirements.txt
    > python ./guides/oauth/authorization.py CLIENT_ID CLIENT_SECRET API_KEY

where CLIENT\_ID refers to your client identity, CLIENT\_SECRET refers to the client secret, and API\_KEY is the key generated through the Surveymonkey console. 

This will launch an OAuth dialog in your default browser to allow a user to log into SurveyMonkey, and also launch a simple web server that will process one request (which is the redirection from the OAuth dialog).

After the user enters their credentials and authorizes the app, SurveyMonkey will redirect to your local webserver, which will then exchange the short-lived access code it receives for a long-lived access token.

PLEASE NOTE: In order for this to proper work, the redirect\_uri on your Mashery Application must be http://127.0.0.1:8000 for this application to work. It is important that the Mashery redirect\_uri refer to your local host, so this might be different depending on how you've configured your /etc/hosts file.
