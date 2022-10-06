from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from unittest import skip
import sys

class FunctionalTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        
        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                return
        super().tearDownClass()

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn(row_text, [row.text for row in rows])


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Home page test
        self.browser.get(self.server_url)
        header_text = self.browser.find_element(By.TAG_NAME,'h1').text
        self.assertIn('To-Do', self.browser.title)
        self.assertIn('To-Do', header_text)

        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'), 
            'Enter a to-do item')
        
        #Post request 1
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID,'id_list_table'))) 

        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # Post request 2
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)


        WebDriverWait(self.browser, 10).until(
            EC.staleness_of(self.browser.find_element(By.ID,'id_list_table'))) 
        edith_list_url = self.browser.current_url

        self.assertRegex(edith_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

        # Init
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # check list not show
        self.browser.get(self.server_url)
        page_text = self.browser.find_element(By.ID, 'id_new_item').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Post request 3
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID,'id_list_table'))) 
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # self.fail('Finish the test')



class LayoutAndStylingTest(FunctionalTest):
    
    def test_layout_and_styling(self):

        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=10)

        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=10)

        
class ItemVaildaionTest(FunctionalTest):
    
    @skip
    def test_cannot_add_empty_list_items(self):
        self.fail("write me")