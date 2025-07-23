from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from _self_packages import send
import time

class Site_Taiwanjobs():
    """
    在指定的台灣就業通網址中抓取職缺資料
    """
    def __init__(self, driver:webdriver.Chrome, url:str, page_number:int=1):
        self.driver = driver
        self.page_number = page_number
        self.url = url
    
    def load_page(self):
        """
        載入指定的網址，台灣就業通不能修改頁碼
        """
        send.message(f"正在載入台灣就業通第{self.page_number}頁...")
        self.driver.get(self.url)

    def next_page(self):
        """
        按下'載入更多'讀取下一頁的內容
        """
        try:
            next_page_button = WebDriverWait(self.driver, timeout=10, poll_frequency=0.5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f'div#plPageLinkRight > a'))
            )
            self.page_number += 1
            send.message(f"正在載入台灣就業通第{self.page_number}頁...")
            next_page_button.click()

            # 確認目前的頁數是否大於應該要載入的頁數
            for wait in range(1, 3):
                print(f"正在等待頁面載入: {wait}/3")
                last_page_number = self.driver.find_elements(By.CSS_SELECTOR, f"li.t-paginations")[-1].get_attribute("data-pages")
                if int(last_page_number) < self.page_number:
                    time.sleep(3)
        except:
            return -1

        
    def scraping(self):
        """
        抓取目前的頁面資料整理後，以list格式回傳
        """
        try:
            item_eles = WebDriverWait(self.driver, timeout=10, poll_frequency=0.5).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, f'ul.search-list-items li.search-list-item'))
            )
        except:
            return -1

        # 資料擷取
        jobs_list = []
        for item in item_eles:
            # 職缺ID
            hire_id = item.get_attribute("id").replace("hire_", "")

            # 企業ID
            employer_href = item.find_element(By.CSS_SELECTOR, "a.t-card-comp-name").get_attribute("href")
            target_idx = employer_href.index("EMPLOYER_ID=")
            employer_id = employer_href[target_idx : employer_href.index("&", target_idx)].replace("EMPLOYER_ID=", "")

            # 其他資訊
            title = item.find_element(By.CSS_SELECTOR, "div a.text-inherit").text
            company = item.find_element(By.CSS_SELECTOR, "div a.t-card-comp-name").text
            job_content = item.find_element(By.CSS_SELECTOR, "div.t-list-substance").text
            area = item.find_element(By.CSS_SELECTOR, "li.t-card-area").text
            salary = item.find_element(By.CSS_SELECTOR, "li.t-list-txts-item text.t-money").text
            education = item.find_element(By.CSS_SELECTOR, "li.t-card-edu").text
            experience = item.find_element(By.CSS_SELECTOR, "li.t-card-workexp").text
            update = item.find_element(By.CSS_SELECTOR, "text.t-list-date").text

            job = {
                "連結": f"https://job.taiwanjobs.gov.tw/Internet/Index/JobDetail.aspx?EMPLOYER_ID={employer_id}&HIRE_ID={hire_id}",
                "標題": title,
                "企業": company,
                "地區": area,
                "薪資": salary,
                "學歷": education,
                "經驗": experience,
                "說明": job_content,
                "更新": update,
            }
            
            jobs_list.append(job)
        
        return jobs_list