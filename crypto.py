import logging
import urllib.request
import json

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

data = urllib.request.urlopen('https://koinex.in/api/ticker').read()
data = json.loads(data)
coins = ['BTC', 'XRP', 'ETH', 'BCH', 'LTC']

def build_response(message):
	return {
		"speech": message,
		"displayText": message
	}
	
	
def get_coin_price(intent_request):
	output_session_attributes = intent_request['result']['contexts'] if intent_request['result']['contexts'] is not None else {}
	parameters = intent_request['result']['parameters']
	coin = parameters['coins']
	if coin in coins:
		price = data['prices'][coin]
		price_min = data['stats'][coin]['min_24hrs']
		price_max = data['stats'][coin]['max_24hrs']
		response = 'Current price of {} is {}. Last 24 hours --> Min: {} and Max: {}'.format(coin, price, price_min, price_max)
	else:
		response = ''
		for coin in coins:
			resp = '{}: {} '.format(coin, data['prices'][coin])
			response = response + resp
	return build_response(response)
	
	
def dispatch(intent_request):
	logger.debug('dispatch userId={}'.format(intent_request['id']))
	intent_name = intent_request['result']['metadata']['intentName']
	# Dispatch to your bot's intent handlers
	if intent_name == 'CoinsPrice':
		return get_coin_price(intent_request)
	raise Exception('Intent with name ' + intent_name + ' not supported')

	
def lambda_handler(event, context):
	logger.debug('Request: {}'.format(event))
	return dispatch(event)