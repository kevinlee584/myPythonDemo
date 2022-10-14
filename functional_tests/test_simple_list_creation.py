from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Home page test
        self.browser.get(self.server_url)
        header_text = self.browser.find_element(By.TAG_NAME,'h1').text
        self.assertIn('To-Do', self.browser.title)
        self.assertIn('To-Do', header_text)

        inputbox = self.get_item_input_box()
        self.assertEqual(
            inputbox.get_attribute('placeholder'), 
            'Enter a to-do item')
        
        #Post request 1
        inputbox.send_keys('Buy peacock feathers', Keys.ENTER)
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # Post request 2
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Use peacock feathers to make a fly', Keys.ENTER)

        edith_list_url = self.browser.current_url

        self.assertRegex(edith_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

        # Init
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # check list not show
        self.browser.get(self.server_url)
        page_text = self.get_item_input_box().text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Post request 3
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy milk', Keys.ENTER)

        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # self.fail('Finish the test')