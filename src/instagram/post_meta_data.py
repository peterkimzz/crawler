import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

# from modules.SeleniumDriver import selenium
# from modules.Slack.slack import Slack
from modules.slack import Slack
from modules.selenium import Selenium

if __name__ == '__main__':

    # driver = Selenium().driver

    slack = Slack()
    slack.send_message('우와')
    # slack.chat.post_message('#notifiactions', '우와')
