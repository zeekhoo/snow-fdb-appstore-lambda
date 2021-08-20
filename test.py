import handler
import json
import sys
import os

def test1():
  eventBody = '{\n    "data": [\n        [0, "zee.khoo@fauna.com"]\n    ]\n}'
  body = json.loads(eventBody)
  event = {
    'queryStringParameters': {
      'email': 'zee.khoo@fauna.com'
    },
    'headers': {
      'Authorization': 'Bearer {}'.format(os.getenv("FAUNADB_SECRET"))
    },
    'body': eventBody
  }
  res = handler.handle_event(event, None)
  print(res['body'])

test1()