from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import url_revision


def search(driver:webdriver.Chrome, url:str, page=1) -> list:
    """
    進入1111網址抓取工作資料，整理後以list格式回傳。
    """
    # 修改網址中的頁碼
    url = url_revision.page_number(url=url, page=page)
    
    driver.get(url=url)

    item_eles = WebDriverWait(driver, timeout=10, poll_frequency=0.5).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, f'div.search-content div.job-card'))
    )

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
        