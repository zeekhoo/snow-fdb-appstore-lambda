import os
from urllib.parse import urlparse
import sys
from faunadb import query as q
from faunadb.client import FaunaClient
import json

secret = os.getenv("FAUNADB_SECRET")
endpoint = os.getenv("FAUNADB_ENDPOINT")

if not secret:
  print("The FAUNADB_SECRET environment variable is not set, exiting.")
  sys.exit(1)

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
    email = event['queryStringParameters']['email']
  except:
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
#   event = {
#     'queryStringParameters': {
#       'email': 'zee.khoo@fauna.com'
#     }
#   }
#   res = handle_event(event, None)
#   print(res['body'])

# test1()