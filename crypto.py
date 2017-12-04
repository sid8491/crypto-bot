import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def build_response(message):
    return {
		"speech": message,
		"displayText": message
	}
	
def lambda_handler(event, context):
	coin = event['result']['parameters']['coins']
	return build_response(coin)