import json
import settings
import time
from _self_packages.chrome_driver import ChromeDriver


url = r"https://www.104.com.tw/jobs/search/?area=6001001000&jobsource=joblist_search&mode=s&page=1"

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

log = chrome_driver.request_log()
for obj in log:
    # print(obj["請求網址"])
    if "https://www.104.com.tw/jobs/search/api/jobs" in obj["請求網址"]:
        print(obj["請求網址"])
        result = json.loads(obj["回傳內容"]["body"])

jobs = result["data"]
print(jobs)
print(type(jobs))
print(len(jobs))