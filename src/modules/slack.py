from slacker import Slacker


class Slack():
    def __init__(self):

        token = 'xoxb-363734903206-431926758755-BO6XrPDrPlx4pHz6Onc13ZrZ'
        slack = Slacker(token)

        self.slack = slack

    def send_message(self, text=None, channel='#notifications', attachments=None):

        self.slack.chat.post_message(
            text=text, channel=channel, attachments=attachments)
