from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions
from unittest import TestCase
import unittest

class NewVisitorTest(TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get("http://localhost:8000")
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME,'h1').text
        self.assertIn('To-Do', header_text)


        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'), 
            'Enter a to-do item')
        
        table = self.browser.find_element(By.ID, 'id_list_table')

        inputbox.send_keys('buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)

        wait = WebDriverWait(table, 10)
        wait.until(expected_conditions.staleness_of(table))

        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn('1: Buy peacock feathers', [row.text for row in rows])

        # attempts = 0
        # while attempts < 2:
        #     try:
        #         table = self.browser.find_element(By.ID, 'id_list_table')
        #         rows = table.find_elements(By.TAG_NAME, 'tr')
        #         self.assertIn('1: Buy peacock feathers', [row.text for row in rows])
        #         break

        #     except StaleElementReferenceException:
        #         attempts+=1

        self.fail('Finish the test')


if __name__ == '__main__':
    unittest.main(warnings='ignore')