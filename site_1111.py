from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import url_revision
from self_packages import send
import settings

class Site_1111():
    """
    在指定的1111網址中抓取職缺資料
    """
    def __init__(self, driver:webdriver.Chrome, page_number:int=1):
        self.driver = driver
        self.page_number = page_number
        self.url = settings.url["1111"]
    
    def load_page(self, page:int|None=None):
        """
        載入指定的網址，可利用page=修改頁碼
        """
        if page is not None and page != self.page_number:
            self.page_number = page
        send.message(f"正在載入1111第{self.page_number}頁...")

        url = url_revision.page_number(url=self.url, page=self.page_number) # 修改網址中的頁碼
        self.driver.get(url)

    def next_page(self):
        """
        載入下一頁
        """
        self.page_number += 1
        self.load_page()
        
    def scraping(self):
        """
        抓取目前的頁面資料整理後，以list格式回傳
        """
        try:
            item_eles = WebDriverWait(self.driver, timeout=10, poll_frequency=0.5).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, f'div.search-content div.job-card'))
            )
        except:
            return -1

        # 資料擷取
        jobs_list = []
        for item in item_eles:
            id = item.get_attribute("data-purpose")
            all_h2_eles = item.find_elements(By.CSS_SELECTOR, "h2")
            title = all_h2_eles[0].text
            company = all_h2_eles[1].text
            job_content = item.find_elements(By.CSS_SELECTOR, "p")[1].text

            other_info = item.find_elements(By.CSS_SELECTOR, ".job-card-condition .job-card-condition__text")
            area = other_info[0].text
            salary = other_info[1].text
            education = other_info[2].text
            experience = other_info[3].text

            update = item.find_element(By.CSS_SELECTOR, "div.job-summary").text
            update = update.replace(" ", "")[:5] # 刪除應徵人數資訊

            job = {
                "連結": f"https://www.1111.com.tw/job/{id}",
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
        