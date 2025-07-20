import json
import settings
import time
from _self_packages.chrome_driver import ChromeDriver
from _self_packages import send
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

url = r"https://www.1111.com.tw/search/job?page=1&col=da&sort=desc&c0=100100"

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
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, f'div.search-content div.job-card'))
)

# 資料擷取
for item in item_eles:
    print("-------")
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

    info = {
        "連結": f"https://www.1111.com.tw/job/{id}",
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