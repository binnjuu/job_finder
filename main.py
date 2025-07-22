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

page_number = 1
jobs_list = []
while page_number <= MAX_PAGE_LIMIT:
    print(f"正在載入第{page_number}頁")
    load_page(url=settings.url["104"], page=page_number)
    jobs_list += site_104.scraping()

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

print(f"共找到: {len(jobs_list)}筆資料")

# 篩選出還未儲存的當日職缺
filter_jobs_list = []
for job in jobs_list:
    if jobs_list[-1]["更新"] != date:
        continue
    elif not data_check.json_file(jobs_list[-1]):
        filter_jobs_list.append(job)

# 整理後送出discord訊息
bot_message_list = []
for job in filter_jobs_list:
    bot_message = f"\n### {job["更新"]} | [{job["標題"]}]({job["連結"]})\n"
    bot_massage += f"```[企業] {job["企業"]}\n"
    bot_massage += f"[地區] {job["地區"]}\n"
    bot_massage += f"[學歷] {job["學歷"]}\n"
    bot_massage += f"[經驗] {job["經驗"]}\n"
    bot_massage += f"[薪資] {job["薪資"]}\n"
    bot_massage += f"[說明]\n{job["說明"]}```"
    bot_message_list.append(bot_massage)
kawaii_fox.start(api_key=settings.discord_bot_key, channel_id=settings.channel_id, message=bot_message_list)

# today_json.write(content=new_jobs_104)