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

    def write(self, content: dict):
        """
        依據今天的日期輸出json file
        ex. 2025-07-21.json
        """
        path = self.today_json_path()
        open(path, encoding="utf8", mode="w+").write(send.pretty(content, enable_print=False))
    
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

        