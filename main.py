import settings
from _self_packages.chrome_driver import ChromeDriver
from _self_packages import send

import site_1111
import site_104
import site_taiwanjobs

#監聽Chrome Driver
chrome_driver = ChromeDriver(port=settings.port, driver_path=settings.driver_path, profile_save_path=settings.profile_save_path)
while True:
    if not chrome_driver.check_port():
        chrome_driver.launch(account=settings.account)
    else:
        break

driver = chrome_driver.monitor()

jobs_1111 = site_1111.search(driver=driver, url=site_1111.url)
# send.pretty(jobs_1111)

jobs_104 = site_104.search(driver=driver, url=site_104.url)
# send.pretty(jobs_104)

jobs_taiwanjobs = site_taiwanjobs.search(driver=driver, url=site_taiwanjobs.url)
# send.pretty(jobs_taiwanjobs)

all_jobs = {
    "104": jobs_104,
    "1111": jobs_1111,
    "taiwanjobs": jobs_taiwanjobs,
}
send.pretty(all_jobs)