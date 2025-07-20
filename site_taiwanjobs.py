import json
import settings
import time
from _self_packages.chrome_driver import ChromeDriver
from _self_packages import send
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

url = r"https://job.taiwanjobs.gov.tw/Internet/Index/job_search_list.aspx?qStamp=638885484970095899"

#監聽Chrome Driver
chrome_driver = ChromeDriver(port=settings.port, driver_path=settings.driver_path, profile_save_path=settings.profile_save_path)
while True:
    if not chrome_driver.check_port():
        chrome_driver.launch(account=settings.account)
    else:
        break

driver = chrome_driver.monitor()

driver.get(url)
time.sleep(3)

item_eles = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, f'ul.search-list-items li.search-list-item'))
)

# 資料擷取
for item in item_eles:
    print("-------")
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

    info = {
        "連結": f"https://job.taiwanjobs.gov.tw/Internet/Index/JobDetail.aspx?EMPLOYER_ID={employer_id}&HIRE_ID={hire_id}",
        "標題": title,
        "企業": company,
        "地區": area,
        "薪資": salary,
        "學歷": education,
        "經驗": experience,
        "工作內容": job_content,
        "更新": update,
    }
    
    send.pretty(info)