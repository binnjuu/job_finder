import settings
from _self_packages.chrome_driver import ChromeDriver
from _self_packages import send
from datetime import datetime
import time

from today_json import Today_Json
from site_104 import Site_104
import data_check

MAX_PAGE_LIMIT = 3

#監聽Chrome Driver
chrome_driver = ChromeDriver(port=settings.port, driver_path=settings.driver_path, profile_save_path=settings.profile_save_path)
while True:
    if not chrome_driver.check_port():
        chrome_driver.launch(account=settings.account)
    else:
        break

driver = chrome_driver.monitor()

today_json = Today_Json()
site_104 = Site_104(driver=driver)

date = str(datetime.today().date())[-5:].replace("-", "/") # 取得今天的日期，格式: 07/21

page_104 = 1
jobs_104 = []
while page_104 <= MAX_PAGE_LIMIT:
    print(f"正在載入第{page_104}頁")
    site_104.load_page(url=settings.url["104"], page=page_104)
    jobs_104 += site_104.scraping()

    # 如果資料抓取失敗或是沒有資料則中斷
    if len(jobs_104) <= 0:
        print("資料抓取失敗或是沒有資料")
        break
    # 如果最後一筆資料不是當天的則中斷
    elif jobs_104[-1]["更新"] != date:
        print("最後一筆資料不是當天的")
        break
    # 如果最後一筆資料已經儲存在json檔案中則中斷
    elif data_check.json_file(jobs_104[-1]):
        print("最後一筆資料已經儲存在json檔案")
        break

    # 否則繼續抓取下一頁
    page_104 += 1
    time.sleep(3) # 避免載入頻率過高

# send.pretty(jobs_104)
print(f"共找到: {len(jobs_104)}筆資料")
today_json.write(content=jobs_104)