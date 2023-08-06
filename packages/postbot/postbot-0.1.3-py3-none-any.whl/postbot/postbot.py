import time
import logging

from .db import MySqlClient
from .util import validate_args

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class PostBot:
    """Class to be instantiated to use the lib. Required arguments are 'geckodriver_path'
    (can download from https://github.com/mozilla/geckodriver/releases), 'username' and 'password'
     for the Instagram account. Optional parameters are MySQL database parameters. This is used in case that posts'
     content are stored in a DB and want to post them every a certain time interval"""

    def __init__(
            self,
            geckodriver_path: str = None,
            delay: int = 10,
            username: str = None,
            password: str = None,
            **kwargs
    ):
        self.use_mysql = False
        self.log_level = logging.INFO
        self.delay = delay
        self.username = username
        self.password = password
        self.state = 0

        for key, val in kwargs.items():
            if key == 'log_level':
                self.log_level = val
            if key.startswith('mysql_'):
                self.use_mysql = True

        logging.basicConfig(level=self.log_level)

        ok = validate_args(geckodriver_path, username, password, kwargs, self.use_mysql)
        if not ok:
            return

        user_agent = "Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16"
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", user_agent)
        self.browser = webdriver.Firefox(executable_path=geckodriver_path, firefox_profile=profile)

        if self.use_mysql:
            self.mysql_client = MySqlClient(kwargs.get('mysql_host'),
                                            kwargs.get('mysql_username'),
                                            kwargs.get('mysql_password'),
                                            kwargs.get('mysql_database'),
                                            kwargs.get('mysql_posts_table'),
                                            kwargs.get('mysql_img_path_column'),
                                            kwargs.get('mysql_caption_txt_column'),
                                            )

        self.browser.get('https://www.instagram.com')

    def login(self):
        """Login to Instagram using the credentials provided"""

        self.click_btn('Log In')
        user = self.browser.find_element_by_xpath("//input[@name='username']")
        passwd = self.browser.find_element_by_xpath("//input[@name='password']")
        user.send_keys(self.username)
        passwd.send_keys(self.password)
        passwd.submit()
        self.click_btn('Not Now')
        logging.info("Successfully logged in")

    def create_post(self, img_path: str, caption_text: str):
        """Creates a single post using the image at the img_path provided and the caption text"""

        self.upload_image(img_path)
        self.click_btn('Next')
        self.write_caption(caption_text)
        # TODO tag people, add filters
        self.click_btn('Share')
        logging.info("Post created successfully")

    def start_posting(self, post_interval_in_min: int = 30):
        """Creates posts using data from MySQL database and according to the interval passed in post_interval_in_min"""

        if not self.use_mysql:
            logging.error("Need MySQL database configuration to use start_posting() function")
            self.browser.quit()
            return
        while True:
            posts = self.mysql_client.get_posts_data()
            if posts is None:
                logging.error("Error occurred in MySQL database while trying to retrieve posts")
                self.browser.quit()
                break
            if len(posts) == 0:
                break
            for post in posts:
                img_path = post[1]
                caption_txt = post[2]
                self.create_post(img_path, caption_txt)
                self.mysql_client.update_to_posted(post[0])
                time.sleep(post_interval_in_min * 60)

    def create_one_post(self, add_caption_intro: str = ""):
        """Creates only one post using data from MySQL database"""

        if not self.use_mysql:
            logging.error("Need MySQL database configuration to use create_one_post() function. Maybe want to use create_post() function.")
            self.browser.quit()
            return
        post = self.mysql_client.get_one_post_data()
        if post is None:
            logging.error("Error occurred in MySQL database while trying to retrieve posts")
            self.browser.quit()
            return
        if len(post) == 0:
            return

        img_path = post[0][1]
        caption_txt = post[0][2]
        if add_caption_intro != "":
            caption_txt = add_caption_intro + post[0][2]

        self.create_post(img_path, caption_txt)
        self.mysql_client.update_to_posted(post[0][0])


    def upload_image(self, img_path: str):
        try:
            self.click_btn_by_xpath("//div[@data-testid='new-post-button']")
            upload = self.browser.find_element_by_xpath("//input[@type='file']")
            upload.send_keys(img_path)

        except TimeoutException:
            self.browser.quit()
            logging.error("Loading took too much time while uploading image!")
            raise

    def write_caption(self, caption_text: str):
        try:
            text_area = WebDriverWait(self.browser, self.delay).until(
                EC.presence_of_element_located((By.TAG_NAME, "textarea")))
            text_area.send_keys(caption_text)

        except TimeoutException:
            self.browser.quit()
            logging.error("Loading took too much time while trying to write caption!")
            raise

    def quit(self):
        try:
            self.click_btn_by_xpath("//div[@data-testid='new-post-button']")
            self.browser.quit()

        except TimeoutException:
            self.browser.quit()
            logging.error("Loading took too much time while trying to close browser!")
            raise

    def click_btn(self, btn_text: str):
        try:
            btn_to_click = WebDriverWait(self.browser, self.delay).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(text(), '" + btn_text + "')]")))
            btn_to_click.click()

        except TimeoutException:
            self.browser.quit()
            logging.error("Loading took too much time while trying to click button " + btn_text + "!")
            raise

    def click_btn_by_xpath(self, xpath: str):
        try:
            btn_to_click = WebDriverWait(self.browser, self.delay).until(
                EC.presence_of_element_located((By.XPATH, xpath)))
            btn_to_click.click()

        except TimeoutException:
            self.browser.quit()
            logging.error("Loading took too much time while trying to click button by xpath!")
            raise
