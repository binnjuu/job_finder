from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
import socket
import json
from _self_packages import send

class ChromeDriver:
    """
    chrome driver相關函式
    """
    def __init__(self, port:str|int, driver_path:str, profile_save_path:str, enable_headless:bool=False) -> None:
        self.port = port
        self.driver_path = driver_path
        self.profile_save_path = profile_save_path
        self.enable_headless = enable_headless
        self.driver = None


    def check_port(self) -> bool:
        """
        利用檢查通訊埠是否開啟來確認瀏覽器的啟動狀態
        來源: https://stackoverflow.com/questions/70764097/how-can-i-ping-a-specific-port-and-report-the-results
        """
        timeout=3
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #presumably 
        sock.settimeout(timeout)
        try:
            sock.connect((f"127.0.0.1", int(self.port)))
        except:
            return False # port未開啟
        else:
            sock.close()
            return True # port已開啟

    
    def launch(self, account:str | None = None) -> None:
        """
        啟動Chrome瀏覽器
        """
        if self.check_port():
            print(f"{self.port}已啟動")
            return
        
        try:
            print(f"正在啟動chrome driver, port:{self.port}")
            path = '"chrome"'
            has_account = "" if account is None else rf"\{account}"
            userdata = rf'"{self.profile_save_path}{has_account}\profile\chromeprofile"'
            diskcache = rf'"{self.profile_save_path}{has_account}\profile\chromecache"'

            if self.enable_headless:
                path += ' --headless=new'

            path += f' --remote-debugging-port={self.port} --user-data-dir={userdata} --disk-cache-dir={diskcache}'

            os.system(f'start "chrome" {path}')

        except Exception as e:
            send.pause(text="啟動Chrome瀏覽器發生錯誤...", e=e)
        

    def monitor(self) -> webdriver.Chrome:
        """
        監聽已啟動的Chrome瀏覽器
        """
        if self.driver is not None: return self.driver
        
        try:
            if not self.check_port():
                print(f"監聽失敗，無法連線到{self.port}...")
                return None

            service = Service(executable_path = self.driver_path) #chromedriver路徑
            
            # 參數設定
            options = webdriver.ChromeOptions()
            options.set_capability('goog:loggingPrefs', {'performance': 'ALL'}) # 用於取得Network介面資料
            options.add_experimental_option("debuggerAddress", f'127.0.0.1:{self.port}')

            self.driver = webdriver.Chrome(service=service, options=options)
            return self.driver
            
        except Exception as e:
            send.pause(text="監聽Chrome瀏覽器發生錯誤...", e=e)

        
    def request_log(self) -> list:
        """
        從瀏覽器取得request記錄
        儲存成list格式回傳

        來源:https://gist.github.com/lorey/079c5e178c9c9d3c30ad87df7f70491d
        """
        if self.driver is None:
            send.error_message("請先監聽chrome driver")
            return
        
        try:
            logs_raw = self.driver.get_log("performance")
            logs = [json.loads(lr["message"])["message"] for lr in logs_raw]

            def log_filter(log_):
                return (
                    # is an actual response
                    log_["method"] == "Network.responseReceived"
                    # and json
                    and "json" in log_["params"]["response"]["mimeType"]
                )

            request_log = []
            for log in filter(log_filter, logs):
                request_id = log["params"]["requestId"]
                resp_url = log["params"]["response"]["url"]
                response = self.driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})
                # print("\n----------------------------------------------\n")
                # print(resp_url)
                # print(response)
                request_log.append({
                    "請求網址": resp_url,
                    "回傳內容": response,
                })
            
            return request_log
        
        except Exception as e:
            send.pause(text="取得request記錄發生錯誤...", e=e)
            return None
    

    def get_headers_data(self, url:str, load_page=True) -> {str, str}:
        """
        取得指定頁面的cookie與user agent，並以str格式回傳
        """
        if self.driver is None:
            send.error_message("請先監聽chrome driver")
            return
        
        try:
            if load_page:
                self.driver.get(url)
                self.driver.implicitly_wait(5) # 最多等待載入秒數

            # 取得Cookie並轉為Dict格式
            cookies_list = self.driver.get_cookies()
            cookies_dict = {}
            for cookie in cookies_list:
                cookies_dict[cookie['name']] = cookie['value']
            # print(cookies_dict)

            #將Cookie轉為傳輸時的格式
            cookie_string = "; ".join([str(x)+"="+str(y) for x,y in cookies_dict.items()])
            # print(cookie_string)

            # 取得UserAgent
            userAgent = str(self.driver.execute_script("return navigator.userAgent;"))

            return cookie_string, userAgent
        
        except Exception as e:
            send.pause(text="取得指定頁面headers資料發生錯誤...", e=e)
            return None, None


if __name__ == '__main__':
    port = 9000
    driver_path = "../../driver/chromedriver.exe"
    profile_save_path = r"D:\Users\User\Desktop"

    chrome_driver = ChromeDriver(port=port, driver_path=driver_path, profile_save_path=profile_save_path)
    chrome_driver.launch(account="test_profile")

    driver = chrome_driver.monitor()
    driver.get("https://www.google.com/")
    