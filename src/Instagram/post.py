import argparse
import datetime
import os
import time
from selenium import webdriver
from sys import platform

__author__ = "Peter Kim"
__version__ = "0.1"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_URL = "https://www.instagram.com/explore/tags"
