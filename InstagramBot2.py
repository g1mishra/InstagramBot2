from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

from returnPassword import getPassword

delay = 10


class InstagramBot:
    def __init__(self):
        self.url = "https://instagram.com"
        self.const_str = "liked your"
        # script will exclude the given date type
        self.const_date = []  # day -> 1d, 3d.. week -> 1w, 2w

    def openAndLogin(self):
        time.sleep(3)
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get(self.url)
        time.sleep(5)
        username = self.driver.find_element_by_css_selector("form#loginForm input[type='text']")
        username.send_keys("g1_mishra")
        password = self.driver.find_element_by_css_selector("form#loginForm input[type='password']")
        password.send_keys(getPassword())  # getPasseord() : return "password"
        # hit enter to login
        password.send_keys(Keys.ENTER)
        time.sleep(5)
        # notification pop-up
        WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[type]")))
        self.driver.find_elements_by_css_selector("button[type]")[-1].click()
        WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[tabindex]")))
        self.driver.find_elements_by_css_selector("button[tabindex]")[-1].click()
        time.sleep(5)

    # likeAndCommentPosts(driver)
    def getWhoLikedPosts(self):
        self.driver.get(f"{self.url}/accounts/activity/")
        time.sleep(5)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        divContainer = soup.find("main")
        listOfNotification = divContainer.find_all("div", attrs={"tabindex": True})
        self.user_who_liked = []
        for x in listOfNotification:
            if x.text.find(self.const_str) > -1:
                user = x.text.split(" ")[0]
                day = x.text.split(".")[-1]
                user = {"user_name": user}
                print(day, user)
                if (day[-1] not in self.const_date) and (user not in self.user_who_liked):
                    self.user_who_liked.append(user)
        print(self.user_who_liked)

    def sendMessgae(self):
        for user in self.user_who_liked:
            self.driver.get(f"{self.url}/direct/new/")
            send_to = self.driver.find_elements_by_css_selector("input[type]")[-1]
            send_to.send_keys(user["user_name"])
            WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[aria-disabled]")))
            self.driver.find_elements_by_css_selector("div[aria-disabled]")[0].click()
            WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[type] > div")))
            self.driver.find_elements_by_css_selector("button[type] > div")[3].click()
            WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div > textarea")))
            message_box = self.driver.find_elements_by_css_selector("div > textarea")[0]
            message_box.send_keys("thank you for all the likes, I'm a bot")
            message_box.send_keys(Keys.ENTER)
        time.sleep(10)
        self.driver.quit()


if __name__ == "__main__":
    obj = InstagramBot()
    obj.openAndLogin()
    obj.getWhoLikedPosts()
    obj.sendMessgae()
