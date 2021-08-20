import os
from urllib.parse import urlparse
import sys
from faunadb import query as q
from faunadb.client import FaunaClient
import json

secret = os.getenv("FAUNADB_SECRET")
endpoint = os.getenv("FAUNADB_ENDPOINT")
endpoint = endpoint or "https://db.fauna.com/"

o = urlparse(endpoint)

client = FaunaClient(
  secret=secret,
  domain=o.hostname,
  port=o.port,
  scheme=o.scheme
)

# lightweight function that simply calls the GetSecureJoinSettingsByOwner UDF.
# The UDF takes 1 parameter: email
def getSecureJoinSettingsByOwner(email):
  result = client.query(
    q.call(q.function('GetSecureJoinSettingsByOwner'), email)
  )
  return result['data']

def handle_event(event, context):
  try:
    # secret = event['headers']['Authorization'].split('Bearer ')[1]
    requestBody = json.loads(event['body'])
    requestData = requestBody['data']
    email = requestData[0][1]
  except Exception as e:
    print(e)
    email = None
  print('email={}'.format(email))

  res = []
  try:
    if email:
      res.append([0, getSecureJoinSettingsByOwner(email)])
  except Exception as e:
    print(e)

  return {
    'statusCode': 200,
    'body': json.dumps({ 'data': res })
  }

# def test1():
#   eventBody = '{\n    "data": [\n        [0, "zee.khoo@fauna.com"]\n    ]\n}'
#   body = json.loads(eventBody)
#   event = {
#     'queryStringParameters': {
#       'email': 'zee.khoo@fauna.com'
#     },
#     'headers': {
#       'Authorization': 'Bearer {}'.format(os.getenv("FAUNADB_SECRET"))
#     },
#     'body': eventBody
#   }
#   res = handle_event(event, None)
#   print(res['body'])

# test1()