from selenium import webdriver


class Selenium:

    def __init__(self):

        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
        options.add_argument("lang=ko_KR")

        # driver = webdriver.Chrome(
        #     r"C:\Users\peter\Desktop\dev\assets\drivers/chromedriver.exe", options=options)

        driver = webdriver.Chrome(
            '/Users/donghyunkim/dev/drivers/chromedriver', options=options)

        driver.implicitly_wait(3)
        self.driver = driver
