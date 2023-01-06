from selenium.webdriver.common.by import By
class Sbs:
    def current_page_items(self, item_list): #전체페이지에서 각 기사의 링크, 메타데이터 저장해둠
        try:
            all_items_ul = self.driver.find_element(By.XPATH, "//*[@id='container']/div[2]/div[2]/ul")
            all_items = all_items_ul.find_elements(By.TAG_NAME, "li")
            for meta in all_items:
                meta_url = meta.find_element(By.XPATH, "meta[contains(@itemprop, 'mainEntityOfPage')]")
                item_url = meta_url.get_attribute("itemid")
                
                meta_author = meta.find_element(By.XPATH, "meta[contains(@itemprop, 'author')]")
                item_author = meta_author.get_attribute("content")
                
                meta_date = meta.find_element(By.XPATH, "meta[contains(@itemprop, 'datePublished')]")
                item_date = meta_date.get_attribute("content")
                
                meta_headline = meta.find_element(By.XPATH, "meta[contains(@itemprop, 'headline')]")
                item_headline = meta_headline.get_attribute("content")

                item_list.append([item_url, item_author, item_date, item_headline])
        except Exception:
            return False
    
    def get_news_content(self, driver): #각 기사에서 뉴스 전문 가져옴
        text_area = driver.find_element(By.CLASS_NAME, "text_area")
        content = text_area.get_attribute("innerText")
        return content