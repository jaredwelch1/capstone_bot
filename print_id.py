import os
from slackclient import SlackClient

BOT_NAME = 'capstone_bot'

slack_client = SlackClient(os.environ.get('token'))

if __name__ == "__main__":
	api_call = slack_client.api_call("users.list")
	if api_call.get('ok'):
		# get list of all the users to find bot
		users = api_call.get('members')
		for user in users:
			if 'name' in user and user.get('name') == BOT_NAME:
				print("Found bot, ID is" + user.get('id'))

