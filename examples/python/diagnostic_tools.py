#! /usr/bin/python
# Very basic script demonstrating diagnostic tools functionality
#
import requests, logging, json
from random import randint
from akamai.edgegrid import EdgeGridAuth
from config import EdgeGridConfig
from urlparse import urljoin
import urllib
session = requests.Session()
debug = False


# If all parameters are set already, use them.  Otherwise
# use the config
config = EdgeGridConfig({"verbose":debug},"default")

if config.verbose or config.debug:
  debug = True


# Set the config options
session.auth = EdgeGridAuth(
            client_token=config.client_token,
            client_secret=config.client_secret,
            access_token=config.access_token
)

# Set the baseurl based on config.host
baseurl = '%s://%s/' % ('https', config.host)

def getResult(endpoint, parameters=None):
  if parameters:
    parameter_string = urllib.urlencode(parameters)
    path = ''.join([endpoint + '?',parameter_string])
  else:
    path = endpoint
  endpoint_result = session.get(urljoin(baseurl,path))
  if debug: print ">>>\n" + json.dumps(endpoint_result.json(), indent=2) + "\n<<<\n"
  return endpoint_result.json()

def postResult(endpoint, body, parameters=None):
  headers = {'content-type': 'application/json'}
  if parameters:
          parameter_string = urllib.urlencode(parameters)
          path = ''.join([endpoint + '?',parameter_string])
  else:
          path = endpoint
  endpoint_result = session.post(urljoin(baseurl,path), data=body, headers=headers)
  if debug: print ">>>\n" + json.dumps(endpoint_result.json(), indent=2) + "\n<<<\n"
  return endpoint_result.json()

def putResult(endpoint, body, parameters=None):
  headers = {'content-type': 'application/json'}
  if parameters:
          parameter_string = urllib.urlencode(parameters)
          path = ''.join([endpoint + '?',parameter_string])
  else:
          path = endpoint
  endpoint_result = session.put(urljoin(baseurl,path), data=body, headers=headers)
  if debug: print ">>>\n" + json.dumps(endpoint_result.json(), indent=2) + "\n<<<\n"
  return endpoint_result.json()


# Request locations that support the diagnostic-tools
print
print "Requesting locations that support the diagnostic-tools API.\n"

location_result = getResult('/diagnostic-tools/v1/locations')

# Select a random location to host our request
location_count = len(location_result['locations'])

print "There are %s locations that can run dig in the Akamai Network" % location_count
rand_location = randint(0, location_count)
location = location_result['locations'][rand_location]
print "We will make our call from " + location + "\n"

# Request the dig request the {OPEN} Developer Site IP informantion
print "Running dig from " + location
dig_parameters = { "hostname":"developer.akamai.com", "location":location, "queryType":"A" }
dig_result = getResult("/diagnostic-tools/v1/dig",dig_parameters)

# Display the results from dig
print dig_result['dig']['result']
