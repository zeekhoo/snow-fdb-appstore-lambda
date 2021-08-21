import os
from urllib.parse import urlparse
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


# ------------------------------------------------------------------------------------------------
# handler #2: This one does inserts
# See example: https://docs.fauna.com/fauna/current/tutorials/indexes/#create-documents
# ------------------------------------------------------------------------------------------------
def populateResults(arr):
  result = client.query(
    q.map_(
      q.lambda_(
        ['rownum', 'userId', 'hashedEmail', 'linkId'],
        q.create(
          q.collection('Results'),
          {
            'data': {
              'userId': q.var('userId'),
              'hashedEmail': q.var('hashedEmail'),
              'linkId': q.var('linkId')
            }
          }
        )
      ),
      arr
    )
  )
  return result

def handle_insert_event(event, context):
  try:
    requestBody = json.loads(event['body'])
    requestData = requestBody['data']
  except Exception as e:
    print('malformed request: {}'.format(e))
    return {
      'statusCode': 400,
      'body': json.dumps({'data': [[0, {'error': ''.format(e)}]]})
    }
  try:
    if len(requestData) > 0:
      res = populateResults(requestData)
      inputCheck = []
      for item in requestData:
        inputCheck.append(item[1])
      body = []
      i = 0
      for item in res:
        userId = item['data']['userId']
        if userId in inputCheck:
          body.append([i, 'Added userId {}'.format(userId)])
        else:
          body.append([i, 'Failed to add userId {}'.format(userId)])
        i += 1
      print('body: {}'.format(list(body)))
      return {
        'statusCode': 200,
        'body': json.dumps({'data': body})
      }
    else:
      print('no data')
      return { 'statusCode': 204 }    
  except Exception as e:
    print('FQL exception: {}'.format(e))
    return { 
      'statusCode': 500,
      'body': json.dumps({'data': [[0, {'error': ''.format(e)}]]})
    }


