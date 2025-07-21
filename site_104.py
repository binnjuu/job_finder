from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import url_revision


class Site_104():
    """
    在指定的104網址中抓取職缺資料
    """
    def __init__(self, driver:webdriver.Chrome):
        self.driver = driver

    def load_page(self, url:str, page=1):
        """
        載入指定的網址，可利用page=修改頁碼
        """
        url = url_revision.page_number(url=url, page=page) # 修改網址中的頁碼
        self.driver.get(url)

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

            job = {
                "連結": link,
                "標題": title,
                "企業": company,
                "地區": area,
                "薪資": salary,
                "學歷": education,
                "經驗": experience,
                "工作內容": job_content,
                "更新": update,
            }
            
            jobs_list.append(job)
        
        return jobs_list