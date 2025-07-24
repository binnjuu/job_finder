from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from self_packages import send
import other.url_revision as url_revision
import setting.settings as settings

class Site_518():
    """
    在指定的518網址中抓取職缺資料
    """
    def __init__(self, driver:webdriver.Chrome, page_number:int=1):
        self.driver = driver
        self.page_number = page_number
        self.url = settings.url["518"]
    
    def load_page(self, page:int|None=None):
        """
        載入指定的網址，518不能修改頁碼
        """
        if page is not None and page != self.page_number:
            self.page_number = page
        send.message(f"正在載入518第{self.page_number}頁...")

        url = url_revision.page_number(url=self.url, arg="job-index-P-",page=self.page_number) # 修改網址中的頁碼
        self.driver.get(url)

    def next_page(self):
        """
        按下'載入更多'讀取下一頁的內容
        """
        self.page_number += 1
        self.load_page()
    
    def scraping(self):
        """
        抓取目前的頁面資料整理後，以list格式回傳
        """
        try:
            item_eles = WebDriverWait(self.driver, timeout=10, poll_frequency=0.5).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, f'div#listTableArea div.all_job_hover > div.job__card'))
            )
        except:
            return -1

        # 資料擷取
        jobs_list = []
        for item in item_eles:
            # 其他資訊
            link = item.find_element(By.CSS_SELECTOR, "h2.job__title__inner > a.job__title").get_attribute("href")
            title = item.find_element(By.CSS_SELECTOR, "h2.job__title__inner > a.job__title").text

            company = item.find_element(By.CSS_SELECTOR, "span.job__comp__name").text
            job_content = item.find_element(By.CSS_SELECTOR, "p.job__intro").text
            salary = item.find_element(By.CSS_SELECTOR, "p.job__salary").text

            other = item.find_elements(By.CSS_SELECTOR, "ul.job__summaries > li")
            area = other[0].text
            experience = other[1].text
            education = other[2].text
            update = item.find_element(By.CSS_SELECTOR, "span.job__date").text

            job = {
                "連結": link,
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
        
        # 移除最後兩個建議職缺
        jobs_list = jobs_list[:-2]
        return jobs_list