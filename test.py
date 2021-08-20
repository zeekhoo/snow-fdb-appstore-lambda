from handler import handle_event, handle_insert_event
import os

def test1():
  eventBody = '{\n    "data": [\n        [0, "zee.khoo@fauna.com"]\n    ]\n}'
  event = {
    'body': eventBody
  }
  res = handle_event(event, None)
  print(res['body'])

def test2():
  # eventBody = '{"data": {}}'
  eventBody = '{\n    "data": [\n        [0, "123", "hash@email.hash", "linkid"],\n        [1, "678", "md5hashbaby", "linqlinkleenk"]\n    ]\n}'
  # eventBody = '{\n    "data": [\n        [0, "123", "hash@email.hash", "linkid"],\n    ]\n}'
  event = {
    'body': eventBody
  }
  res = handle_insert_event(event, None)

test2()