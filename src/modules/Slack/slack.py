from slacker import Slacker


class Slack():
    def __init__(self):

        token = 'xoxb-363734903206-431926758755-BO6XrPDrPlx4pHz6Onc13ZrZ'
        slack = Slacker(token)
        print('Slacker is created.')
        self = slack

    def send_message(text=None, channel='#notifications', attachments=None):

        self.chat.post_message(text=text, channel=channel,
                               attachments=attachments)
