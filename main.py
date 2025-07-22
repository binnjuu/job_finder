import settings
from _self_packages.chrome_driver import ChromeDriver
from _self_packages import kawaii_fox
from _self_packages import send
from datetime import datetime
import time

from today_json import Today_Json
from site_104 import Site_104
from site_1111 import Site_1111
from site_taiwanjobs import Site_Taiwanjobs
import data_check
import url_revision

MAX_PAGE_LIMIT = 1

#監聽Chrome Driver
chrome_driver = ChromeDriver(port=settings.port, driver_path=settings.driver_path, profile_save_path=settings.profile_save_path)
while True:
    if not chrome_driver.check_port():
        chrome_driver.launch(account=settings.account)
    else:
        break

driver = chrome_driver.monitor()

def load_page(url:str, page=1):
    """
    載入指定的網址，可利用page=修改頁碼
    """
    url = url_revision.page_number(url=url, page=page) # 修改網址中的頁碼
    driver.get(url)

today_json = Today_Json()
site_104 = Site_104(driver=driver)
site_1111 = Site_1111(driver=driver)
site_taiwanjobs = Site_Taiwanjobs(driver=driver)

date = str(datetime.today().date())[-5:].replace("-", "/") # 取得今天的日期，格式: 07/21

def scraping_data(site_key):
    page_number = 1
    jobs_list = []
    while page_number <= MAX_PAGE_LIMIT:
        print(f"正在讀取{site_key}網站第{page_number}頁...")
        if site_key == "taiwanjobs":
            driver.get(settings.url[site_key])
        else:
            load_page(url=settings.url[site_key], page=page_number)
        jobs_list += site_list[site_key]()

        # 如果資料抓取失敗或是沒有資料則中斷
        if len(jobs_list) <= 0:
            print("資料抓取失敗或是沒有資料")
            break
        # 如果最後一筆資料不是當天的則中斷
        elif jobs_list[-1]["更新"] != date:
            print("最後一筆資料不是當天的")
            break
        # 如果最後一筆資料已經儲存在json檔案中則中斷
        elif data_check.json_file(jobs_list[-1]):
            print("最後一筆資料已經儲存在json檔案")
            break

        # 否則繼續抓取下一頁
        page_number += 1
        time.sleep(3) # 避免載入頻率過高
    
    return jobs_list


site_list = {
    "104": site_104.scraping,
    "1111": site_1111.scraping,
    "taiwanjobs": site_taiwanjobs.scraping,
}

all_jobs = {}
for key in site_list.keys():
    all_jobs[key] = scraping_data(key)
    print(f"在{key}共找到{len(all_jobs[key])}筆資料")


# 篩選出還未儲存的當日職缺
all_filter_jobs = {}
for key in all_jobs.keys():
    jobs_list = all_jobs[key]
    for job in jobs_list:
        if job["更新"] != date:
            continue
        elif not data_check.json_file(job):
            if key not in all_filter_jobs.keys():
                all_filter_jobs[key] = []
            all_filter_jobs[key].append(job)

# 整理後送出discord訊息
bot_message_list = []
for filter_jobs in all_filter_jobs.values():
    for job in filter_jobs:
        bot_message = f"\n### {job["更新"]} | [{job["標題"]}](<{job["連結"]}>)\n"
        bot_message += f"```[企業] {job["企業"]}\n"
        bot_message += f"[地區] {job["地區"]}\n"
        bot_message += f"[學歷] {job["學歷"]}\n"
        bot_message += f"[經驗] {job["經驗"]}\n"
        bot_message += f"[薪資] {job["薪資"]}\n"
        bot_message += f"[說明]\n{job["說明"]}```"
        bot_message_list.append(bot_message)
if len(bot_message_list) > 0:
    print(f"共篩選出{len(bot_message_list)}個職缺資訊")
    kawaii_fox.start(api_key=settings.discord_bot_key, channel_id=settings.channel_id, message=bot_message_list)

# 每次抓完資料都會替換json內容為最新的資料，再看要不要改成新增的
today_json.write(content=all_jobs)