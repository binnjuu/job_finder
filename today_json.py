import os
import json
from datetime import datetime
from _self_packages import send

class Today_Json():
    def __init__(self, dir_path:str="./file"):
        self.dir_path = dir_path

        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)

    def today_json_path(self):
        today = datetime.today().date()
        path = f'{self.dir_path}/{today}.json'
        return path

    def save(self, new_jobs_list: dict):
        """
        依據今天的日期輸出json file
        如果已經建立了則改為新增內容
        ex. 2025-07-21.json
        """
        path = self.today_json_path()
        if not os.path.isfile(path):
            open(path, encoding="utf8", mode="w+").write(send.pretty(new_jobs_list, enable_print=False))
            return
        
        data = self.read()
        for site_key in new_jobs_list.keys():
            if site_key not in data.keys():
                data[site_key] = []
            
            data[site_key] += new_jobs_list[site_key]
        open(path, encoding="utf8", mode="w+").write(send.pretty(data, enable_print=False))
    
    def read(self):
        """
        讀取並回傳今天的json file
        """
        path = self.today_json_path()
        if os.path.isfile(path):
            json_content = open(path, encoding="utf8", mode="r").read()
            return json.loads(json_content)
        else:
            return -1 # 檔案不存在則回傳-1

        