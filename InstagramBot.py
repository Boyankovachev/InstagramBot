from selenium import webdriver
import os
import time


class InstagramBot:

    def __init__(self, username, password):
        """
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
        accept_cookies = self.driver.find_element_by_xpath("/html/body/div[2]/div/div/div/div[2]/button[1]")
        accept_cookies.click()
        time.sleep(1)
        username_tab = self.driver.find_element_by_xpath("""//*[@id="loginForm"]/div/div[1]/div/label/input""")
        password_tab = self.driver.find_element_by_xpath("""//*[@id="loginForm"]/div/div[2]/div/label/input""")
        username_tab.send_keys(self.username)
        password_tab.send_keys(self.password)
        login_button = self.driver.find_element_by_xpath("""//*[@id="loginForm"]/div/div[3]""")
        login_button.click()
        time.sleep(3)
        login_info_button = self.driver.find_element_by_xpath(
            """//*[@id="react-root"]/section/main/div/div/div/div/button""")
        login_info_button.click()
        time.sleep(1)
        notifications_button = self.driver.find_element_by_xpath("""/html/body/div[4]/div/div/div/div[3]/button[2]""")
        notifications_button.click()

    def navigate_to_home_page(self):
        """
        Opens the home page,
        once user is logged in
        """
        self.driver.get("https://www.instagram.com/" + self.username + "/")

    def get_following_number(self):
        """
        When on home page,
        read number of followings
        """
        following_num = self.driver.find_element_by_xpath(
            """//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/span""")
        self.number_of_followings = following_num.text
        


class UnfollowUsers(InstagramBot):
    def open_following_tab(self):
        """
        opens the following tab when
        located in the profile tab:
        """
        following_buttom = self.driver.find_element_by_xpath(
            """//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a""")
        following_buttom.click()

    def get_following(self, num_to_scrape=10):
        """'
        on having the following insta tab open
        stores the usernames of the users in a list
        Args:
            num_to_scrape - how much usernames to read
        """
        if num_to_scrape < 0:
            return

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

        self.following_list = following_list_


instagram = UnfollowUsers("nema da mi", "kradesh instata ei")
time.sleep(1)
instagram.login()
time.sleep(1)
instagram.navigate_to_home_page()
time.sleep(1)
instagram.get_following_number()
print(instagram.number_of_followings)
time.sleep(5)
instagram.driver.quit()
