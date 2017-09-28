import os
import time
from slackclient import SlackClient
import datetime
from _thread import *
import requests

class capstone_bot(object):

	def __init__(self):
		# starterbot's ID as an environment variable
		BOT_ID = os.environ.get("bot_id")
		
		# constants
		self.AT_BOT = "<@" + BOT_ID +">"
		
		# instantiate Slack & Twilio clients
		self.slack_client = SlackClient(os.environ.get('token'))

		self.valid_commands = ['report']

		# list of coin symbols loaded from local .conf 
		self.tracked_coins = ['BTC', 'ETH', 'WTC', 'OMG', 'NEO', 'GAS']		

		self.api_url = 'https://api.coinmarketcap.com/v1/ticker/'

	def start(self):
		READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
		if self.slack_client.rtm_connect():
			
			targetDate = datetime.datetime.now()
			targetHour = targetDate.hour
						
 			# self.startMessage()

			while True:
				if datetime.datetime.now().hour > targetHour:
					# num_articles = get_articles_count()
					targetDate += datetime.timedelta(hours = 1)
					targetHour = targetDate.hour
					self.postReport()


				output = self.parse_slack_output(self.slack_client.rtm_read())
				if output:
					start_new_thread(self.handle_command,(output,))
					time.sleep(READ_WEBSOCKET_DELAY)
	    		
			
		else:
			print("Connection failed. Invalid Slack token or bot ID?")	
		
	def handle_command(self, output):
		"""
		Receives commands directed at the bot and determines if they
		are valid commands. If so, then acts on the commands. If not,
		returns back what it needs for clarification.

		output - a dict with slack output information 
		"""
		# get list of text after the @ mention, separated by white space
		text = output['text'].split(self.AT_BOT)[1].split()
		# text = list(filter(None, text))
	
		# expected format: <command> <args...>
		
		command = text[0] 
		args = text[1:]

		if command in self.valid_commands:
			
			if command == 'report':
				if args[0] in self.tracked_coins:
					self.postReport(output['channel'], args[0])
				else:
					self.postReport(output['channel'])
		

	    # slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

	def parse_slack_output(self,slack_rtm_output):
		"""
		The Slack Real Time Messaging API is an events firehose.
		this parsing function returns None unless a message is
		directed at the Bot, based on its ID.
		"""
		output_list = slack_rtm_output
		if output_list and len(output_list) > 0:
			for output in output_list:
				if output and 'text' in output and self.AT_BOT in output['text']:
					return output
		return None
	
	def postReport(self, channel, symbol=None):
		r = requests.get(self.api_url)
		coins = r.json()
		message = ''
		report_coins = []
		
		if symbol is None:
			for c in coins:
				if c['symbol'] in self.tracked_coins:
					report_coins.append(c)
			for c in report_coins:		
					sym = c['symbol']				
					vol_24 = '$'
					vol_24 += c['24h_volume_usd']
					ch_7d = c['percent_change_7d']
					ch_7d += '%'				
					ch_24h = c['percent_change_24h']
					ch_24h += '%'				
					ch_1h = c['percent_change_1h']
					btc_val = c['price_btc']
					usd_val = c['price_usd']
				
					message = '{:3}: \n\t 24hr change: {:5} \n\t btc val: {:14} \n\t USD: ${:6}'.format(sym, ch_24h, btc_val, usd_val) 
					self.slack_client.api_call("chat.postMessage", channel=channel, text=message, as_user=True)
		else:
			for c in coins:
				if c['symbol'] == symbol:
					sym = c['symbol']				
					vol_24 = '$'
					vol_24 += c['24h_volume_usd']
					ch_7d = c['percent_change_7d']
					ch_7d += '%'				
					ch_24h = c['percent_change_24h']
					ch_24h += '%'				
					ch_1h = c['percent_change_1h']
					btc_val = c['price_btc']
					usd_val = c['price_usd']
				
					message = '{:3}: \n\t 24hr change: {:5} \n\t btc val: {:14} \n\t USD: ${:6}'.format(sym, ch_24h, btc_val, usd_val) 
					self.slack_client.api_call("chat.postMessage", channel=channel, text=message, as_user=True)
# this function will query the database for total articles and return it 

# def get_articles_count():
	



if __name__ == "__main__":
	capstone_bot().start()
