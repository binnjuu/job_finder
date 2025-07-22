from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver


class Site_Taiwanjobs():
    """
    在指定的1111網址中抓取職缺資料
    """
    def __init__(self, driver:webdriver.Chrome):
        self.driver = driver
        
    def scraping(self):
        """
        抓取目前的頁面資料整理後，以list格式回傳
        """
        item_eles = WebDriverWait(self.driver, timeout=10, poll_frequency=0.5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, f'ul.search-list-items li.search-list-item'))
        )

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