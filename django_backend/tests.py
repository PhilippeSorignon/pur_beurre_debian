from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import time


class SearchTestCase(LiveServerTestCase):

    def setUp(self):
        """Setup the test driver and create test users"""

        self.driver = webdriver.Firefox()
        self.wait = WebDriverWait(self.driver, 1000)

    def tearDown(self):
        self.driver.quit()


    def test_search(self):
        self.driver.get("http://localhost:3000")

        self.wait.until(lambda driver: self.driver.find_element_by_class_name("form-control").is_displayed())

        self.driver.find_element_by_class_name("form-control").send_keys("nutella")

        self.driver.find_element_by_link_text("Chercher").click()

        self.wait.until(lambda driver: self.driver.find_element_by_class_name("card-title").is_displayed())

        result = self.driver.find_element_by_class_name("card-title").text

        assert "Nutella" in result


    def test_connect(self):
        self.driver.get("http://localhost:3000")

        self.wait.until(lambda driver: self.driver.find_element_by_class_name("form-control").is_displayed())

        self.driver.find_element_by_link_text("Connexion").click()

        self.wait.until(lambda driver: self.driver.find_element_by_name("username").is_displayed())

        self.driver.find_element_by_name("username").send_keys("Test")
        self.driver.find_element_by_name("password").send_keys("test")
        ActionChains(self.driver).key_down(Keys.RETURN).key_up(Keys.RETURN).perform()

        self.wait.until(lambda driver: self.driver.find_element_by_link_text("Chercher").is_displayed())

        self.driver.find_element_by_class_name("form-control").send_keys("nutella")

        self.driver.find_element_by_link_text("Chercher").click()

        self.wait.until(lambda driver: self.driver.find_element_by_class_name("card-title").is_displayed())

        result = self.driver.find_element_by_class_name("btn-primary").text

        assert "Sauvegarder" in result
