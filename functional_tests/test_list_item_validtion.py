from unittest import skip

from selenium.common.exceptions import (NoSuchElementException,
                                        StaleElementReferenceException)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from .base import FunctionalTest


class ItemVaildaionTest(FunctionalTest):
    
    def get_error_element(self):
        exception = None
        for i in range(5):
            try:
                error = self.browser.find_element(By.CSS_SELECTOR, '.has-error')
                return error
            except NoSuchElementException as e:
                exception = e
            except StaleElementReferenceException as e:
                exception = e
        
        raise exception

    def test_cannot_add_empty_list_items(self):
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        error = self.get_error_element()
        self.assertEqual(error.text, "You can't have an empty list item")

        self.get_item_input_box().send_keys('Buy milk', Keys.ENTER)
        self.check_for_row_in_list_table('1: Buy milk')

        self.get_item_input_box().send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1: Buy milk')
        error = self.get_error_element()
        self.assertEqual(error.text, "You can't have an empty list item")

        self.get_item_input_box().send_keys('Make tea', Keys.ENTER)
        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: Make tea')
    
    def test_cannot_add_deplicate_items(self):

        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('Buy wellies', Keys.ENTER)
        self.check_for_row_in_list_table('1: Buy wellies')

        self.get_item_input_box().send_keys('Buy wellies', Keys.ENTER)
        self.check_for_row_in_list_table('1: Buy wellies')
        error = self.get_error_element()
        self.assertEqual(error.text, "You've already got this in your list")

    def test_error_message_are_cleaned_on_input(self):
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)
        error = self.get_error_element()
        self.assertTrue(error.is_displayed())

        self.get_item_input_box().send_keys('a')
        error = self.get_error_element()
        self.assertFalse(error.is_displayed())
        