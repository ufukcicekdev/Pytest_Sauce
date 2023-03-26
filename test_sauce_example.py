from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
import pytest
from pathlib import Path
from datetime import date
from locators import *
import uuid


class Test_Sauce_Work:
    def setup_method(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.maximize_window()
        self.driver.get("https://www.saucedemo.com/")
        self.folderPath = str(date.today())
        self.uuidId = uuid.uuid4()
        Path(self.folderPath).mkdir(exist_ok=True) #klasör yapısı

    def teardown_method(self):
        self.driver.quit()

    def test_username_and_password_empty_message(self):
        metot_name ="test_username_and_password_empty_message"
        self.waitForElemtVisibil((By.ID,INPUT_USERNAME)) 
        self.waitForElemtVisibil((By.ID,INPUT_PASSWORD))
        self.login_buttton_click()
        erormessages = self.driver.find_element(By.XPATH,ERROR_MESSAGE_TEXT)
        self.driver.save_screenshot(f"{self.folderPath}/{metot_name}-{self.uuidId}.png")
        assert  erormessages.text == "Epic sadface: Username is required"

    @pytest.mark.parametrize("username",[("test2_kullanici"),("test1_kullanici"),("test3_kullanici")]) # ilgili parametler için teker teker kullanır
    def test_password_empty_message(self,username):
        metot_name = "test_password_empty_message"
        self.waitForElemtVisibil((By.ID,INPUT_USERNAME)) 
        usernameeinput = self.driver.find_element(By.ID,"user-name")
        usernameeinput.send_keys(username)
        self.login_buttton_click()
        erormessages = self.driver.find_element(By.XPATH,ERROR_MESSAGE_TEXT)
        self.driver.save_screenshot(f"{self.folderPath}/{metot_name}-{self.uuidId}.png")
        assert  erormessages.text == "Epic sadface: Password is required"


    def test_locked_out_message(self):
        metot_name ="test_locked_out_message"
        self.waitForElemtVisibil((By.ID,INPUT_USERNAME)) 
        usernameeinput = self.driver.find_element(By.ID,"user-name")
        self.waitForElemtVisibil((By.ID,INPUT_PASSWORD))
        passwordinput = self.driver.find_element(By.ID,"password")
        usernameeinput.send_keys("locked_out_user")
        passwordinput.send_keys("secret_sauce")
        self.login_buttton_click()
        erormessages = self.driver.find_element(By.XPATH,ERROR_MESSAGE_TEXT)
        self.driver.save_screenshot(f"{self.folderPath}/{metot_name}-{self.uuidId}.png")
        assert  erormessages.text == "Epic sadface: Sorry, this user has been locked out."

    def test_close_icon(self):
        metot_name ="test_close_icon"
        clickbuttoncase = True
        self.waitForElemtVisibil((By.ID,INPUT_USERNAME)) 
        self.waitForElemtVisibil((By.ID,INPUT_PASSWORD))
        self.login_buttton_click()
        self.driver.save_screenshot(f"{self.folderPath}/{metot_name}-{self.uuidId}.png")
        errorBtn = self.driver.find_element(By.XPATH,MESSAGE_CLOSED)
        if errorBtn:
            errorBtn.click()
            assert clickbuttoncase


    def test_valid_login(self):
        metot_name ="test_valid_login"
        self.waitForElemtVisibil((By.ID,"user-name"))  
        usernameeinput = self.driver.find_element(By.ID,"user-name")
        self.waitForElemtVisibil((By.ID,"password"))  
        passwordinput = self.driver.find_element(By.ID,"password")
        usernameeinput.send_keys("standard_user")
        passwordinput.send_keys("secret_sauce")
        self.login_buttton_click()
        erormessages = self.driver.find_elements(By.XPATH,ERROR_MESSAGE_TEXT)
        if len(erormessages) ==0:
            self.driver.save_screenshot(f"{self.folderPath}/{metot_name}-{self.uuidId}.png")
            assert True

        
    def test_product_img_click(self): #kendi testim
        self.test_valid_login() 
        metot_name ="test_product_img_click"
        inventoryItems = self.driver.find_elements(By.CLASS_NAME,INVENTORY_ITEM)
        numberOfInventory = len(inventoryItems)
        for i in range(numberOfInventory):
            finds_img = self.driver.find_elements(By.CSS_SELECTOR,IMG_CLICKED)
            finds_img[i].click()
            sleep(2)
            self.driver.save_screenshot(f"{self.folderPath}/{metot_name}-{self.uuidId}.png")
            self.driver.back()
        
        assert True


    def test_navbar_click(self):  #kendi testim
        self.test_valid_login() 
        metot_name ="test_navbar_click"
        self.waitForElemtVisibil((By.CLASS_NAME,"bm-burger-button"))  
        navbar_btn = self.driver.find_element(By.CLASS_NAME,"bm-burger-button")
        navbar_btn.click()
        navbarItems = self.driver.find_elements(By.CSS_SELECTOR,".bm-menu a[id*='sidebar_link']")
        numberOfInventory = len(navbarItems)
        if  numberOfInventory == 4:
            assert True
        


    def waitForElemtVisibil(self, locator):
        WebDriverWait(self.driver,5).until(ec.visibility_of_element_located(locator))


    def login_buttton_click(self):
        self.waitForElemtVisibil((By.ID,LOGINN_BUTTON))  
        login_btn = self.driver.find_element(By.ID,LOGINN_BUTTON)
        login_btn.click()
