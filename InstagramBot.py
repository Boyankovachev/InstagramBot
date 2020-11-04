from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
import MyLogger
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


def read_profiles():
    """
    :return: list of usernames for the program to
    use
    """
    file = open("profiles.txt", "r")
    users_list = []
    for user in file:
        users_list.append(user.strip())
    return users_list


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
        self.my_logger = MyLogger.MyLogger()

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

    def navigate_to_explore_page(self):
        self.driver.get("https://www.instagram.com")

    def get_following_number(self):
        """
        read number of followings when
        located on any home page
        :returns int value of ↑
        """
        WebDriverWait(self.driver, 4).until(
            EC.presence_of_element_located(
                (By.XPATH, """/html/body/div[1]/section/main"""))
        )
        option1 = False
        option2 = False
        if len(self.driver.find_elements_by_xpath(
                """//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/span""")) > 0:
            option1 = True
        elif len(self.driver.find_elements_by_xpath(
                """/html/body/div[1]/section/main/div/header/section/ul/li[3]/span/span""")) > 0:
            option2 = True
        if option1:
            following_num = self.driver.find_element_by_xpath(
                """//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/span""")
        elif option2:
            following_num = self.driver.find_element_by_xpath(
                """/html/body/div[1]/section/main/div/header/section/ul/li[3]/span/span""")
        else:
            return ""
        temp = " "
        temp = following_num.text
        temp = temp.replace(',', '')
        temp = temp.replace('.', '')
        if "k" in temp:
            temp[len(temp)] = ""
        return int(temp)
        # //*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/span
        # /html/body/div[1]/section/main/div/header/section/ul/li[3]/span/span
        # /html/body/div[1]/section/main/div/ul/li[3]/span/span

    def get_followers_number(self):
        """
        read number of followers when
        located on any home page
        :returns int value of ↑
        """
        WebDriverWait(self.driver, 4).until(
            EC.presence_of_element_located(
                (By.XPATH, """/html/body/div[1]/section/main"""))
        )
        option1 = False
        option2 = False
        if len(self.driver.find_elements_by_xpath(
                """//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span""")) > 0:
            option1 = True
        elif len(self.driver.find_elements_by_xpath(
                """/html/body/div[1]/section/main/div/header/section/ul/li[2]/span/span""")) > 0:
            option2 = True
        if option1:
            following_num = self.driver.find_element_by_xpath(
                """//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span""")
        elif option2:
            following_num = self.driver.find_element_by_xpath(
                """/html/body/div[1]/section/main/div/header/section/ul/li[2]/span/span""")
        else:
            return ""
        temp = " "
        temp = following_num.text
        temp = temp.replace(',', '')
        temp = temp.replace('.', '')
        if "k" in temp:
            temp[len(temp)] = ""
        return int(temp)

    def open_following_tab(self):
        """
        opens the following tab when
        located on any home page
        """
        following_button = WebDriverWait(self.driver, 5).until(
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
            try:
                ul = self.driver.find_element_by_xpath("""/html/body/div[5]/div/div/div[2]/ul""")
            except NoSuchElementException:
                ul = self.driver.find_element_by_xpath("""/html/body/div[4]/div/div/div[2]/ul""")
            li = ul.find_elements_by_tag_name("li")
            # /html/body/div[4]/div/div/div[2]/ul - not such element exception mi hvurli
            # /html/body/div[5]/div/div/div[2]/ul - sega maika mu deba

            following_panel = self.driver.find_element_by_xpath("//div[@class='isgrP']")
            self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',
                                       following_panel)

        try:
            ul = self.driver.find_element_by_xpath("""/html/body/div[5]/div/div/div[2]/ul""")
        except NoSuchElementException:
            ul = self.driver.find_element_by_xpath("""/html/body/div[4]/div/div/div[2]/ul""")
        li = ul.find_elements_by_tag_name("li")

        following_list_ = []
        j = 1
        for item in li:
            if j > num_to_scrape:
                break
            following_list_.append(item.text.split("\n")[0])
            j = j + 1

        return following_list_

    def unfollow_user(self):
        """
        Located on any home page tab
        unfollow user
        """
        try:
            follow_menu_button = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH,
                                                """/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button"""))
            )
            follow_menu_button.click()
        except TimeoutException:
            follow_menu_button = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH,
                                                """/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[3]/div/span/span[1]/button"""))
            )
            follow_menu_button.click()
        try:
            unfollow_button = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, """/html/body/div[5]/div/div/div/div[3]/button[1]"""))
            )
            unfollow_button.click()
            return True
        except TimeoutException:
            try:
                unfollow_button = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, """/html/body/div[4]/div/div/div/div[3]/button[1]"""))
                )
                unfollow_button.click()
                return True
            except TimeoutException:
                return False
        return False

    def follow_user(self):
        """
        located on any home page tab
        follow user
        """
        WebDriverWait(self.driver, 4).until(
            EC.presence_of_element_located(
                (By.XPATH, """/html/body/div[1]/section/main"""))
        )
        option1 = False
        option2 = False
        if len(self.driver.find_elements_by_xpath(
                """/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/button""")) > 0:
            option1 = True
        elif len(self.driver.find_elements_by_xpath(
                """/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/div/span/span[1]/button""")) > 0:
            option2 = True
        else:
            return False
        if option1:
            follow_button = self.driver.find_element_by_xpath(
                """/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/button""")
            if follow_button.text == "Follow" or follow_button.text == "Follow Back":
                follow_button.click()
                return True
            else:
                return False
        elif option2:
            follow_button = self.driver.find_element_by_xpath(
                """/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/div/span/span[1]/button""")
            if follow_button.text == "Follow" or follow_button.text == "Follow Back":
                follow_button.click()
                return True
            else:
                return False
        return False
        # /html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/button
        # /html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/div/span/span[1]/button

        # /html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button   ako veche go sledvam
        # /html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/div/span/span[1]/button      ako nito toi me nito az nego
        # /html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/div/span/span[1]/button      ako toi me sledva az nego ne


class UnfollowUsers(InstagramBot):
    def read_all_user_followings(self, user):
        """
        :param user: user to scrape
        :return: full list of followings
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
            print("check_if_user_follows_back bate except chasta")
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
        num_unfollowed = 0
        while num_to_unfollow > num_unfollowed:
            self.navigate_to_home_page()
            following_list = self.get_following(num_to_unfollow * 10)
            random.shuffle(following_list)
            for user in following_list:
                if max_to_check == -1:
                    if not self.check_if_user_follows_back(user):
                        self.navigate_to_home_page(user)
                        if self.unfollow_user():
                            num_unfollowed = num_unfollowed + 1
                            self.my_logger.log_unfollow(user)
                            if num_unfollowed >= num_to_unfollow:
                                return
                elif max_to_check > 0:
                    self.navigate_to_home_page(user)
                    num_of_following = self.get_following_number()
                    if num_of_following > max_to_check:
                        time.sleep(random.randint(2, 4))
                        self.navigate_to_home_page(user)
                        if self.unfollow_user():
                            num_unfollowed = num_unfollowed + 1
                            self.my_logger.log_unfollow(user)
                            if num_unfollowed >= num_to_unfollow:
                                return
                        time.sleep(random.randint(2, 4))
                    else:
                        if not self.check_if_user_follows_back(user):
                            self.navigate_to_home_page(user)
                            if self.unfollow_user():
                                num_unfollowed = num_unfollowed + 1
                                self.my_logger.log_unfollow(user)
                                if num_unfollowed >= num_to_unfollow:
                                    return
        # kogato trqbva da unfollowne
        # otvarq following taba i preebava sichko kurwata


class FollowUsers(InstagramBot):
    def get_random_user(self):
        """
        :return: a string that is a username
        of a profile to follow from
        """
        temp = read_profiles()
        username = random.choice(temp)
        return username

    def open_random_post(self, username):
        """
        opens a random post from a given
        username homepage. when opened the webpage laods the first 24
        without scrolling in lines of 3
        """
        choice_list = []
        for x in range(1, 9):
            for y in range(1, 4):
                choice_list.append(
                    "/html/body/div[1]/section/main/div/div[3]/article/div[1]/div/div[" + str(x) + "]/div[" + str(
                        y) + "]/a")

        self.navigate_to_home_page(username)
        try:
            image = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, random.choice(choice_list)))
            )
            image.click()
        except TimeoutException:
            choice_list = []
            for x in range(1, 9):
                for y in range(1, 4):
                    choice_list.append(
                        "/html/body/div[1]/section/main/div/div[2]/article/div[1]/div/div[" + str(x) + "]/div[" + str(
                            y) + "]/a")
            image = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, random.choice(choice_list)))
            )
            image.click()

    def scroll(self):
        """
        when opened likes panel
        scroll some
        """
        try:
            likes_panel = WebDriverWait(self.driver, 4).until(
                EC.presence_of_element_located(
                    (By.XPATH, """/html/body/div[6]/div/div/div[2]/div"""))
            )
        except TimeoutException:
            likes_panel = WebDriverWait(self.driver, 4).until(
                EC.presence_of_element_located(
                    (By.XPATH, """/html/body/div[5]/div/div/div[2]/div"""))
            )
        self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',
                                   likes_panel)

    def is_eligible_for_follow(self, followers, following):
        """
        :return: True of ok to follow
                 False if not
        """
        if followers > 5000 or following > 2500:
            # print(1, end=": ")
            return False
        if following > 1000 and followers < following * 0.5:
            # print(2, end=": ")
            return False
        if followers < 10 or following < 20:
            # print(3, end=": ")
            return False
        flag = False
        if float(followers) > following * 1.5:
            if followers < 100 and following < followers * 4:
                flag = True
            if 200 > followers >= 100:
                if following < followers * 2:
                    flag = True
            if not flag:
                # print(4, end=": ")
                return False
        return True

    def start_following(self, num_to_follow):
        """
        once logged in,
        open post and start following
        people with the checks and all...
        """
        num_followed = 0

        while num_followed < num_to_follow:
            # opens a random post
            self.open_random_post(self.get_random_user())

            # open likes panel
            try:
                likes_button = WebDriverWait(self.driver, 4).until(
                    EC.presence_of_element_located(
                        (By.XPATH, """/html/body/div[5]/div[2]/div/article/div[3]/section[2]/div/div[2]/button"""))
                )
            except TimeoutException:
                likes_button = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located(
                        (By.XPATH, """/html/body/div[4]/div[2]/div/article/div[3]/section[2]/div/div[2]/button"""))
                )
            likes_button.click()

            users_list = []
            users_scraped = 0
            temp = 1
            while users_scraped < num_to_follow:
                try:
                    user_element = WebDriverWait(self.driver, 1).until(
                        EC.presence_of_element_located(
                            (By.XPATH, """/html/body/div[6]/div/div/div[2]/div/div/div[""" + str(
                                temp) + """]/div[2]/div[1]/div/span/a"""))
                    )
                    # /html/body/div[6]/div/div/div[2]/div/div/div[1]/div[2]/div[1]/div/span/a
                    # /html/body/div[5]/div/div/div[2]/div/div/div[1]/div[2]/div[1]/div/span/a
                    user = user_element.text
                    if user not in users_list:
                        users_list.append(user)
                        users_scraped = users_scraped + 1
                    temp = temp + 1
                except:
                    temp = 1
                    self.scroll()
                    continue
            """
            users_list.clear()
            users_list = [
                "gibbythesmart",
                "ll.paradise.voyage.ll",
                "_____chillwildlife_____",
                "julia_michels_",
                "nugie1966",
                "p_nath_",
                "ray.shizzle"
            ]
            """

            for user in users_list:
                self.navigate_to_home_page(user)
                if self.is_eligible_for_follow(self.get_followers_number(), self.get_following_number()):
                    if self.follow_user():
                        num_followed = num_followed + 1
                        self.my_logger.log_follow(user)
                        if num_followed >= num_to_follow:
                            break


class Simulate(InstagramBot):
    def scroll(self, direction=True):
        """
        on explore page
        scroll some
        direction = false:
            scroll up
        """
        main_panel = self.driver.find_element_by_xpath("/html/body")
        if direction:
            main_panel.send_keys(Keys.PAGE_DOWN)
        else:
            main_panel.send_keys(Keys.PAGE_UP)

    def simulate(self, num_to_like):
        """
        once logged in
        simulate scrolling and liking
        """
        time.sleep(2)
        last_post = ""
        num_of_posts_liked = 0
        while num_of_posts_liked < num_to_like:
            for x in range(4):
                self.scroll()
                time.sleep(random.randint(1, 2))
            article = self.driver.find_element_by_tag_name("article")
            links = article.find_elements_by_tag_name("a")
            print(links[1].text)
            if links[1].text == last_post:
                last_post = links[1].text
                continue
            last_post = links[1].text
            if random.randint(3, 4) == 4:
                print("sea she likne")
                footer_element = article.find_element_by_xpath("div[3]")
                buttons = footer_element.find_elements_by_tag_name("button")
                flag = False
                counter = 0
                while not flag and counter < 3:
                    try:
                        counter = counter + 1
                        buttons[0].click()
                        time.sleep(random.randint(2, 3))
                        flag = True
                        self.my_logger.log_like()
                        num_of_posts_liked = num_of_posts_liked + 1
                    except ElementClickInterceptedException:
                        self.scroll(False)
                        continue


"""
instagram = UnfollowUsers(*read_credentials())
instagram.login()
instagram.start_unfollowing(5, 500)
instagram.driver.quit()
"""
"""
instagram = FollowUsers(*read_credentials())
instagram.login()
instagram.start_following(5)
instagram.driver.quit()
"""
instagram = Simulate(*read_credentials())
instagram.login()
instagram.simulate(3)
"""
1vi probelm - kato scrolva se bugva i ne zarejda sledvashtite
2ri problem - ponqkoga prosto skrolva do dolu i nishto ne prai
(reshenie: dobavi except, koito gi hvashtat logvat gi i produljavat)
!PRAVI GO S IDta I Classove ne sus XPATH !!!!
"""
