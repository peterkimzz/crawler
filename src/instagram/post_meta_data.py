import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from modules.SeleniumDriver import selenium
from modules.Slack import slack

if __name__ == '__main__':

    ss = selenium.Selenium()
    print(ss)

    slack = slack.Slack()
    print(slack)
