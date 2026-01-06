from selenium.webdriver import Firefox
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from django.contrib.auth import get_user_model
import time

class FrontendTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.add_argument("--headless")
        cls.selenium = Firefox(options=options)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login_submit_button(self):

        get_user_model().objects.create_user(username='test', password='test')

        self.selenium.get(f"{self.live_server_url}/login")

        username_input = self.selenium.find_element(By.ID, "id_username")
        username_input.send_keys("test")

        password_input = self.selenium.find_element(By.ID, "id_password")
        password_input.send_keys("test")

        self.selenium.find_element(By.XPATH, '//button[text()="Log In"]').click()

        self.assertIn("/notes/create", self.selenium.current_url)

    def test_preview_button_hides_textarea(self):

        get_user_model().objects.create_user(username='test', password='test')

        self.selenium.get(f"{self.live_server_url}/login")
        self.selenium.find_element(By.ID, "id_username").send_keys("test")
        self.selenium.find_element(By.ID, "id_password").send_keys("test")
        self.selenium.find_element(By.XPATH, '//button[text()="Log In"]').click()

        self.selenium.find_element(By.ID, "button-preview").click()
        time.sleep(1)

        textarea = self.selenium.find_element(By.ID, "md-textarea")

        self.assertIn("display: none;", textarea.get_attribute("style") or "")
