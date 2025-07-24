from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import other.url_revision as url_revision
from self_packages import send
import setting.settings as settings

class Site_104():
    """
    在指定的104網址中抓取職缺資料
    """
    def __init__(self, driver:webdriver.Chrome, page_number:int=1):
        self.driver = driver
        self.page_number = page_number
        self.url = settings.url["104"]

    def load_page(self, page:int|None=None):
        """
        載入指定的網址，可利用page=修改頁碼
        """
        if page is not None and page != self.page_number:
            self.page_number = page
        send.message(f"正在載入104第{self.page_number}頁...")

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
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, f'div.recycle-scroller--item'))
            )
        except:
            return -1

        # 資料擷取
        jobs_list = []
        for item in item_eles:
            # 跳過推薦工作
            try:
                item.find_element(By.CSS_SELECTOR, "i.jb_icon_focus")
                # title = item.find_element(By.CSS_SELECTOR, "div.info-container div.info-job > h2").text
                # print(f"SKIP: {title}")
                continue
            except:
                pass

            link = item.find_element(By.CSS_SELECTOR, "div.info-container div.info-job > h2 > a").get_attribute("href")
            title = item.find_element(By.CSS_SELECTOR, "div.info-container div.info-job > h2").text
            company = item.find_element(By.CSS_SELECTOR, "div.info-container div.info-company > a").text
            job_content = item.find_element(By.CSS_SELECTOR, "div.info-container div.info-description").text
            
            other_info = item.find_elements(By.CSS_SELECTOR, "div.info-container div.info-tags > span.info-tags__text")
            area = other_info[0].text
            experience = other_info[1].text
            education = other_info[2].text
            salary = other_info[3].text

            update = item.find_element(By.CSS_SELECTOR, "div.date-container").text
            # 如果字串長度<5則代表月份沒有補0，所以補上0
            if len(update) < 5:
                update = "0" + update

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
        
        return jobs_list