import settings
from self_packages.chrome_driver import ChromeDriver
from self_packages import kawaii_fox
from self_packages import send
from datetime import datetime
import time
import os

from today_json import Today_Json
from site_104 import Site_104
from site_518 import Site_518
from site_1111 import Site_1111
from site_taiwanjobs import Site_Taiwanjobs
from apscheduler.schedulers.blocking import BlockingScheduler
import data_check


MAX_PAGE_LIMIT = 2
def main():
    #監聽Chrome Driver
    chrome_driver = ChromeDriver(port=settings.driver_port, driver_path=settings.driver_path, profile_save_path=settings.profile_save_path)
    while True:
        if not chrome_driver.check_port():
            chrome_driver.launch(account=settings.forld_name)
        else:
            break

    driver = chrome_driver.monitor()

    today_json = Today_Json()
    site_list = {
        "104": Site_104(driver=driver),
        "1111": Site_1111(driver=driver),
        "518": Site_518(driver=driver),
    }

    date = str(datetime.today().date())[-5:].replace("-", "/") # 取得今天的日期，格式: 07/21

    # 在各個網站抓取職缺資料
    all_jobs = {}
    for key in site_list.keys():
        jobs = []
        site_obj = site_list[key]
        for times in range(MAX_PAGE_LIMIT):
            if times == 0:
                site_obj.load_page()
            else:
                site_obj.next_page()
            jobs_list = site_obj.scraping()
            jobs += jobs_list

            # 檢查要不要載入下一頁
            if not data_check.next_page(jobs_list=jobs_list, date=date):
                break
            time.sleep(3) # 避免載入頻率過高
        all_jobs[key] = jobs
        send.message(f"在{key}網站找到{len(jobs)}個職缺")

    # # taiwanjobs (因為抓取資料的方式不太一樣，所以沒放到site_list裡面)
    # site_taiwanjobs = Site_Taiwanjobs(driver=driver)
    # jobs_taiwanjobs = []
    # for times in range(MAX_PAGE_LIMIT):
    #     if times == 0:
    #         site_taiwanjobs.load_page()
    #     else:
    #         site_taiwanjobs.next_page()
    #     jobs_list = site_taiwanjobs.scraping()
    #     jobs_taiwanjobs = jobs_list # 台灣就業通的所有頁數資料都會在同一個頁面上，所以每次都覆蓋掉舊的資料

    #     #檢查要不要載入下一頁
    #     if not data_check.next_page(jobs_list=jobs_list, date=date):
    #         break
    #     time.sleep(3) # 避免載入頻率過高
    # all_jobs["taiwanjobs"] = jobs_taiwanjobs
    # send.message(f"找到{len(jobs_taiwanjobs)}個")

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
            bot_message = f"### {job["更新"]} | [{job["標題"]}](<{job["連結"]}>)\n"
            bot_message += f"```[企業] {job["企業"]}\n"
            bot_message += f"[地區] {job["地區"]}\n"
            bot_message += f"[學歷] {job["學歷"]}\n"
            bot_message += f"[經驗] {job["經驗"]}\n"
            bot_message += f"[薪資] {job["薪資"]}\n"
            bot_message += f"[說明]\n{job["說明"]}```"
            bot_message_list.append(bot_message)
    if len(bot_message_list) > 0:
        print(f"共篩選出{len(bot_message_list)}個職缺資訊")
        kawaii_fox.start(api_key=settings.discord_api_key, channel_id=settings.channel_id, message=bot_message_list)

    # 每次抓完資料都會替換json內容為最新的資料，再看要不要改成新增的
    today_json.save(new_jobs_list=all_filter_jobs)

    # 關閉所有Chrome瀏覽器
    os.system('taskkill /F /IM chrome.exe')

if __name__ == "__main__":
    # send.message("等待下一個30分時開始重複執行...")
    # scheduler = BlockingScheduler()
    # scheduler.add_job(main, 'cron', minute=30) # 每個小時30分的時候都執行一次
    # scheduler.start()
    main()