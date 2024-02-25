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
        
    def searchAmazonItemInformation(self, search_item,):
        
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

    
    def getAmzonItemInformation(self, items, max_page):
        
        item_name = []
        item_price = []
        no_reviews = []
        
        for i in range(max_page):
            # Find all of the search result elements on the page
            search_results = driver.find_elements(By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')
            
            for result in search_results:
                if items:
                    WebDriverWait(result, 4).until(expected_conditions.visibility_of_element_located((By.XPATH,".//span[@class='a-size-base-plus a-color-base a-text-normal']")))
                    names = result.find_elements(By.XPATH,".//span[@class='a-size-base-plus a-color-base a-text-normal']")
                    
                    for name in names:
                        item_name.append(name.text)
                        
                    try:
                        if len(result.find_elements(By.XPATH,".//span[@class='a-price-whole']"))>0:
                            whole_price = result.find_elements(By.XPATH, './/span[@class="a-price-whole"]')
                            fraction_price = result.find_elements(By.XPATH,'.//span[@class="a-price-fraction"]')
                            item_price.append('.'.join([whole_price[0].text, fraction_price[0].text]))
                        else:
                            item_price.append("0")
                    except:
                        pass
                    
                    try:
                        if len(result.find_elements(By.XPATH,".//span[@class='a-size-base s-underline-text']"))>0:
                            reviews = result.find_elements(By.XPATH,".//span[@class='a-size-base s-underline-text']")
                            for review in reviews:
                                no_reviews.append(review.text)
                        else:
                            no_reviews.append("0")
                    except:
                        pass

        return item_name, item_price, no_reviews

        
    
    def saveResult(self, items, max_page, save_path="C:/Users/aysen/OneDrive/Masaüstü/selenium_amazon/items.xlsx"):
        if items:
            item_name, item_price, no_reviews = self.getAmzonItemInformation(items,  max_page)
            df = pd.DataFrame({"Item Name": item_name, "Price": item_price, "No. of Reviews": no_reviews})

            save_path = os.path.join("output_dir/", save_path)

            df.to_excel(save_path, index=False)
            driver.quit()
            return f"save to xlsx file to {save_path}"
        else:
            driver.quit()
            return f"do not save file to {save_path}"
        
        
        
        
        
    
  
  
"""   
item = AmazonItem()
items= item.searchAmazonItemInformation("mause")
item.getAmzonItemInformation(items, 5)
item.saveResult(items, 2, save_path="yeni6.xlsx")     
"""          
            
            
                
                
