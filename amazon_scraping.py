import os
import selenium
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

driver = webdriver.Chrome()


class AmazonItem:
    url = "https://www.amazon.com.tr/"
    
    def __init__(self):
       pass
        
    def searchAmazonItemInformation(self, search_item):
        
        if search_item != None:
            driver.get(self.url)
            driver.maximize_window()
            
            WebDriverWait(driver, 4).until(expected_conditions.visibility_of_element_located((By.ID,"twotabsearchtextbox")))
            search_box = driver.find_element(By.ID,"twotabsearchtextbox")
            search_box.clear()
            
            search_box.send_keys(search_item)
            
            WebDriverWait(driver, 4).until(expected_conditions.visibility_of_element_located((By.ID,"nav-search-submit-button")))
            search_button = driver.find_element(By.ID,"nav-search-submit-button")
            search_button.click()
            
            WebDriverWait(driver, 4).until(expected_conditions.visibility_of_element_located((By.XPATH,'//div[@data-component-type="s-search-result"]')))
            items = driver.find_elements(By.XPATH,'//div[@data-component-type="s-search-result"]')
            
            return items
        else:
            return 0

    
    def getAmzonItemInformation(self, items):
        
        item_name = []
        item_price = []
        no_reviews = []
        final_list = []
        
        if items != None:
            for item in items:
                
                WebDriverWait(driver, 4).until(expected_conditions.visibility_of_element_located((By.XPATH,".//span[@class='a-size-base-plus a-color-base a-text-normal']")))
                names = item.find_elements(By.XPATH,".//span[@class='a-size-base-plus a-color-base a-text-normal']")
                
                for name in names:
                    item_name.append(name.text)
                    
                try:
                    if len(item.find_elements(By.XPATH,".//span[@class='a-price-whole']"))>0:
                        prices= item.find_elements(By.XPATH,".//span[@class='a-price-whole']")
                        for price in prices:
                            # print('the lenght is ===>',len(price.text))
                            item_price.append(price.text)
                    else:
                        item_price.append("0")
                except:
                    pass
                # reviews = laptop.find_elements(By.XPATH,".//span[@class='a-size-base s-underline-text']")
                
                try:
                    if len(item.find_elements(By.XPATH,".//span[@class='a-size-base s-underline-text']"))>0:
                        reviews = item.find_elements(By.XPATH,".//span[@class='a-size-base s-underline-text']")
                        for review in reviews:
                            # print('the length is===>', len(review.text), review.text)
                            no_reviews.append(review.text)
                    else:
                        no_reviews.append("0")
                except:
                    pass
    

        return item_name, item_price, no_reviews
    
    
    def saveResult(self, items,  save_path="C:/Users/aysen/OneDrive/Masaüstü/selenium_amazon/items.xlsx"):
        if items:
            item_name, item_price, no_reviews = self.getAmzonItemInformation(items)
            df = pd.DataFrame({"Item Name": item_name, "Price": item_price, "No. of Reviews": no_reviews})

            save_path = os.path.join("output_dir/", save_path)

            df.to_excel(save_path, index=False)
            driver.quit()
            return f"save to xlsx file to {save_path}"
        else:
            driver.quit()
            return f"do not save file to {save_path}"
        
        
        
        
        
    
"""   
item = AmazonItem("")
item.searchAmazonItemInformation(driver)
item.getAmzonItemInformation(driver)
item.saveResult(save_path="C:/Users/aysen/OneDrive/Masaüstü/selenium_amazon/items.xlsx")

"""        
            
            
            
                
                
