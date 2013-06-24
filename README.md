# SurveyMonkey Python Guides

This project contains many of the examples you can find on http://developer.surveymonkey.com

To install simply run

  pip install -r requirements.txt 

## OAuth Guide

The oauth walks you through the 3 legged dance and shows you how to exchange a authorization code for a long lived
access token to be used with our APIs.

## Requests Guide

The requests guide picks up from where the OAuth guide left you by making requests with your newly created access token

## Polling Guide

The polling guide takes requests to the next level and provides an example implementation where requests are run
at some interval to update and cache data for almost any kind of integration requiring rollups.
