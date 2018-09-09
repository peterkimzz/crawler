from slacker import Slacker


def slack_notify(text=None, channel='#test', username='알림봇', attachments=None):
    token = 'xoxb-363734903206-431926758755-BO6XrPDrPlx4pHz6Onc13ZrZ'
    slack = Slacker(token)
    slack.chat.post_message(text=text, channel=channel,
                            username=username, attachments=attachments)
