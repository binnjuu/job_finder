import setting.settings as settings
from self_packages.chrome_driver import ChromeDriver
from self_packages import send
from datetime import datetime
import time

from other.today_json import Today_Json
from other import bot
from site_obj.site_104 import Site_104
from site_obj.site_518 import Site_518
from site_obj.site_1111 import Site_1111
from apscheduler.schedulers.blocking import BlockingScheduler
import other.data_check as data_check


MAX_PAGE_LIMIT = 2
def main(loop=True):
    send.message("開始讀取當日新職缺資訊")

    #啟用與監聽Chrome Driver
    chrome_driver = ChromeDriver(port=settings.driver_port, driver_path=settings.driver_path, profile_save_path=settings.profile_save_path)
    while True:
        if not chrome_driver.check_port():
            chrome_driver.launch(account=settings.forld_name)
        else:
            break
    driver = chrome_driver.monitor()
    send.message("已監聽Chrome Driver")
    

    today_json = Today_Json()
    site_list = {
        "104": Site_104(driver=driver),
        "1111": Site_1111(driver=driver),
        "518": Site_518(driver=driver),
    }

    today_date = str(datetime.today().date())[-5:].replace("-", "/") # 取得今天的日期，格式: 07/21

    # 在各個網站抓取職缺資訊
    all_jobs = {} # 用於儲存所有網站找到的職缺資訊
    for key in site_list.keys():
        send.message(f"正在讀取{key}網站職缺資訊...",)
        jobs = []
        site_obj = site_list[key]
        for times in range(MAX_PAGE_LIMIT):
            if times == 0:
                site_obj.load_page()
            else:
                site_obj.next_page()
            jobs_list = site_obj.scraping()
            if jobs_list == -1:
                send.error_message(f"目前頁面讀取元素失敗...")
                break

            send.message(f"在目前頁面找到{len(jobs_list)}個職缺資訊")
            jobs += jobs_list

            # 檢查要不要載入下一頁
            if not data_check.next_page(jobs_list=jobs_list, date=today_date):
                break
            time.sleep(3) # 避免載入頻率過高
        all_jobs[key] = jobs
        send.message(f"在{key}網站共找到{len(jobs)}個職缺資訊")

    # 篩選出還未儲存的當日職缺
    all_filter_jobs = data_check.filter_jobs(all_jobs=all_jobs, date=today_date)
    
    # 計算找到多少個未儲存的當日職缺
    new_jobs_count = 0
    for value in all_filter_jobs.values(): new_jobs_count += len(value)
    send.message(f"共篩選出{new_jobs_count}個當日更新的新職缺資訊!")

    # 整理後送出discord訊息
    send.message(f"正在準備送出Discord訊息...")
    bot.discord_message(all_filter_jobs=all_filter_jobs)

    # 將新找到的職缺資訊記錄到json檔案中
    today_json.save(new_jobs_list=all_filter_jobs)
    send.message(f"已將新的職缺資訊記錄到Json檔案中")

    # 關閉所有Chrome瀏覽器
    # os.system('taskkill /F /IM chrome.exe')
    driver.close()

    
    if loop == True:
        send.message(f"正在等待下一次執行...")
    else:
        send.message(f"執行結束")

if __name__ == "__main__":
    send.message("等待下一個30分時開始重複執行...")
    scheduler = BlockingScheduler()
    scheduler.add_job(main, 'cron', minute=30) # 每個小時30分的時候都執行一次
    scheduler.start()