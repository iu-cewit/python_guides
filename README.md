# SurveyMonkey Python Guides

## Goals

This repository was created to provide working example code which makes use of SurveyMonkey's API. It contains many of the examples you can find on http://developer.surveymonkey.com

The code here is neither a software development kit (SDK) nor a reference implementation. Rather we hope it helps you to learn how to use the API at the most basic level and use what you learn to develop the most appropriate robust code for your specific needs.

## Requirements

- Python 3.3 [weblink](http://www.python.org/getit/releases/3.3.0/)
- pip [weblink](https://pypi.python.org/pypi/pip)
- mechanize [weblink](https://pypi.python.org/pypi/mechanize/)
- requests [weblink](https://pypi.python.org/pypi/requests)
- wsgiref [weblink](https://pypi.python.org/pypi/wsgiref)


To install mechanize, requests, and wsgiref using [pip](https://pypi.python.org/pypi/pip), simply run

```
pip install -r requirements.txt 
```

## Guides

### OAuth Guide

The oauth walks you through the 3 legged dance and shows you how to exchange a authorization code for a long lived
access token to be used with our APIs.

### Requests Guide

The requests guide picks up from where the OAuth guide left you by making requests with your newly created access token

### Polling Guide

The polling guide takes requests to the next level and provides an example implementation where requests are run
at some interval to update and cache data for almost any kind of integration requiring periodic polling.
