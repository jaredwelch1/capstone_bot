import os
import time
from slackclient import SlackClient
import datetime


# starterbot's ID as an environment variable
BOT_ID = os.environ.get("bot_id")
# constants
AT_BOT = "<@" + BOT_ID +">"
Poll_command = "poll"

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('token'))


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """

    '''
    if command.startswith(Poll_command):
        response = "Okay, I received a command for a poll"
        handle_poll(command)
    '''

    # slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)


# this function will query the database for total articles and return it 

# def get_articles_count():
	

def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       		output['channel']
    return None, None


if __name__ == "__main__":
	READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
	if slack_client.rtm_connect():
		print("cap bot connected and running!")
		targetDate = datetime.date.today()
		print(str(targetDate))
		while True:

			if datetime.date.today() == targetDate:
				# num_articles = get_articles_count()
				targetDate += datetime.timedelta(days = 1)
				slack_client.api_call("chat.postMessage", channel='capstone_bot_testing', text="HEY THIS WORKS!", as_user=True)


			command, channel = parse_slack_output(slack_client.rtm_read())
			if command and channel:
				handle_command(command, channel)
				time.sleep(READ_WEBSOCKET_DELAY)
    		
			
	else:
		print("Connection failed. Invalid Slack token or bot ID?")
