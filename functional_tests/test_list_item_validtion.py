from .base import FunctionalTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from unittest import skip

class ItemVaildaionTest(FunctionalTest):
    
    
    def test_cannot_add_empty_list_items(self):
        self.browser.get(self.server_url)
        self.browser.find_element(By.ID, 'id_new_item').send_keys(Keys.ENTER)

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'.has-error'))) 

        error = self.browser.find_element(By.CSS_SELECTOR, '.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        self.browser.find_element(By.ID, 'id_new_item').send_keys('Buy milk', Keys.ENTER)
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID,'id_list_table'))) 
        self.check_for_row_in_list_table('1: Buy milk')

        self.browser.find_element(By.ID, 'id_new_item').send_keys(Keys.ENTER)
        WebDriverWait(self.browser, 10).until(
            EC.staleness_of(self.browser.find_element(By.ID,'id_list_table'))) 
        self.check_for_row_in_list_table('1: Buy milk')
        error = self.browser.find_element(By.CSS_SELECTOR, '.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        self.browser.find_element(By.ID, 'id_new_item').send_keys('Make tea', Keys.ENTER)
        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: Make tea')