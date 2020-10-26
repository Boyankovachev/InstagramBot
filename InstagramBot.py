from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random


def read_credentials():
    """"
    Returns a tuple of
    the username and password
    """
    file = open("credentials.txt", "r")
    username = file.readline()
    temp = username.split(": ")
    username = temp[1]
    if username.endswith("\n"):
        username = username.rstrip("\n")
    password = file.readline()
    temp = password.split(": ")
    password = temp[1]
    if password.endswith("\n"):
        password = password.rstrip("\n")
    file.close()
    return username, password


class InstagramBot:

    def __init__(self, username, password):
        """
        logs in to the owner's account
        :param username: instagram username
        :param password: instagram password
        """
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome('C:\chromedriver.exe')
        self.driver.get("https://www.instagram.com/")

    def login(self):
        """
        login function:
        - open instagram
        - accept all cookies
        - enter credentials
        """
        accept_cookies_wait = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div/div[2]/button[1]"))
        )
        accept_cookies_wait.click()
        login_button = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, """//*[@id="loginForm"]/div/div[3]"""))
        )
        username_tab = self.driver.find_element_by_xpath("""//*[@id="loginForm"]/div/div[1]/div/label/input""")
        password_tab = self.driver.find_element_by_xpath("""//*[@id="loginForm"]/div/div[2]/div/label/input""")
        username_tab.send_keys(self.username)
        password_tab.send_keys(self.password)
        login_button.click()
        login_info_button = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, """//*[@id="react-root"]/section/main/div/div/div/div/button"""))
        )
        login_info_button.click()
        notifications_button_wait = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, """/html/body/div[4]/div/div/div/div[3]/button[2]"""))
        )
        notifications_button_wait.click()

    def navigate_to_home_page(self, user=None):
        """
        Opens to home page,
        once user is logged in
        empty - owner home page
        user - this user's home page
        """
        if user is None:
            self.driver.get("https://www.instagram.com/" + self.username + "/")
        else:
            self.driver.get("https://www.instagram.com/" + user + "/")

    def get_following_number(self):
        """
        read number of followings when
        located on any home page
        :returns int value of ↑
        """
        following_num = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, """//*[@id="react-root"]/section/main/div/header/section/ul
             /li[3]/a/span"""))
        )
        temp = " "
        temp = following_num.text
        temp = temp.replace(',', '')
        return int(temp)

    def open_following_tab(self):
        """
        opens the following tab when
        located on any home page
        """
        following_button = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, """//*[@id="react-root"]/section/main/div/header/section/ul
             /li[3]/a"""))
        )
        following_button.click()

    def get_following(self, num_to_scrape=10):
        """
        :returns list of names of followings
        located on any home page tab
        Args:
            num_to_scrape - how much usernames to read
                -1 to scrape all
        test1 - kato mu dadesh da scrapne vsichki raboti
            ako ne se poqvqt promeni mejduvremenni raboti
        test2 - kato mu dadesh da scrapne all,
            se bugva ako ima promeni v procesa
        """
        time.sleep(2)
        if num_to_scrape == -1:
            num_to_scrape = self.get_following_number()
            time.sleep(1)
        elif num_to_scrape <= 0:
            return

        self.open_following_tab()
        time.sleep(2)

        li = []
        while len(li) < num_to_scrape:
            ul = self.driver.find_element_by_xpath("""/html/body/div[4]/div/div/div[2]/ul""")
            li = ul.find_elements_by_tag_name("li")

            following_pannel = self.driver.find_element_by_xpath("//div[@class='isgrP']")
            self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',
                                       following_pannel)

        ul = self.driver.find_element_by_xpath("""/html/body/div[4]/div/div/div[2]/ul""")
        li = ul.find_elements_by_tag_name("li")

        following_list_ = []
        j = 1
        for item in li:
            if j > num_to_scrape:
                break
            following_list_.append(item.text.split("\n")[0])
            j = j + 1

        # self.following_list = following_list_
        return following_list_

    def unfollow_user(self):
        """
        Located on any home page tab
        unfollow user
        """
        try:
            follow_menu_button = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, """//*[@id="react-root"]/section/main/div/header
            /section/div[1]/div[1]/div/div[2]/div/span/span[1]/button"""))
            )
            follow_menu_button.click()
        except:
            follow_menu_button = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, """/html/body/div[1]/section/main/div/header/section/ul/li[
                3]/a/span"""))
            )
            follow_menu_button.click()
        unfollow_button = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, """/html/body/div[4]/div/div/div/div[3]/button[1]"""))
        )
        unfollow_button.click()


class UnfollowUsers(InstagramBot):
    def read_all_user_followings(self, user):
        """
        :param user: user to scrape
        :return: full list of followers
        """
        self.navigate_to_home_page(user)
        all_user_followings = self.get_following(-1)
        return all_user_followings

    def check_if_user_follows_back(self, user):
        """
        :param user: user to check
        :return: True if following back
                 False if not
        """
        try:
            user_list = self.read_all_user_followings(user)
        except:
            return False
        if self.username in user_list:
            return True
        else:
            return False

    def start_unfollowing(self, num_to_unfollow, max_to_check=-1):
        """"
        :param num_to_unfollow: max_users to unfollow
        :param max_to_check: max follows the users to have
        if max_to_check == -1 doesn't check
        for the program to check if he is following back
        scans num_to_unfollow * 10
        """
        self.login()
        self.navigate_to_home_page()
        following_list = self.get_following(num_to_unfollow * 10)
        random.shuffle(following_list)
        users_unfollowed_counter = 0
        for user in following_list:
            if max_to_check == -1:
                if not self.check_if_user_follows_back(user):
                    users_unfollowed_counter = users_unfollowed_counter + 1
                    self.navigate_to_home_page(user)
                    self.unfollow_user()
            elif max_to_check > 0:
                self.navigate_to_home_page(user)
                following_count = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located(
                        (By.XPATH, """/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span"""))
                )
                num = int(following_count.text.replace(',', ''))
                if num > max_to_check:
                    users_unfollowed_counter = users_unfollowed_counter + 1
                    time.sleep(random.randint(2, 4))
                    self.unfollow_user()
                    time.sleep(random.randint(2, 4))
                else:
                    if not self.check_if_user_follows_back(user):
                        users_unfollowed_counter = users_unfollowed_counter + 1
                        self.navigate_to_home_page(user)
                        self.unfollow_user()
            if users_unfollowed_counter >= num_to_unfollow:
                return


instagram = UnfollowUsers(*read_credentials())
instagram.start_unfollowing(5, 500)
instagram.driver.quit()
"""
1vi probelm - kato scrolva se bugva i ne zarejda sledvashtite
2ri problem - kato scrolva spira da zarejda sledvashtite
3ti problem - ponqkoga prosto skrolva do dolu i nishto ne prai
(reshenie: dobavi except, koito gi hvashtat logvat gi i produljavat)
"""
