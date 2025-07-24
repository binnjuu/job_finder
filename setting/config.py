import configparser
import os
import urllib.parse
from self_packages import send

class Config:
    """
    建立config ini檔案
    """
    def __init__(self, file:str, config_pool:list, dir_path="") -> None:
        self.file = rf"{dir_path}\{file}"
        self.config_pool = config_pool
        self.dir_path = dir_path

    def check(self, print_setting=False) -> None:
        """
        檢查config是否存在，如果不存在或缺少參數則重新建立
        """
        try:
            if not os.path.isdir(self.dir_path): os.makedirs(self.dir_path)

            # 檢查config是否已存在
            parser_read = configparser.ConfigParser()
            if os.path.isfile(self.file):
                parser_read.read(self.file, encoding="utf-8")
                # print(parser_read)
                # print(type(parser_read)

            parser_write = configparser.ConfigParser()
            for section in self.config_pool:
                section_name = section["name"]
                parser_write.add_section(section_name)
                write_file = False
                
                for key in dict(section["item"]).keys():
                    find = False
                    # 檢查參數是否已存在
                    if section_name in parser_read.sections():
                        if key in list(parser_read[section_name]):
                            find = True
                            if print_setting:
                                print(f"{key} = {parser_read[section_name][key]}")
                            parser_write.set(section_name, key, parser_read[section_name][key])
                    
                    if not find:
                        # 沒有找到參數，需要新增參數
                        user_input = input(f"需新增參數{key}...{section['item'][key]}: ")
                        # 避免輸入網址時有ASCII keycode
                        if '%' in user_input:
                            user_input = urllib.parse.unquote(user_input)
                        parser_write.set(section_name, key, user_input)
                        write_file = True

                if write_file:
                    parser_write.write(open(self.file, "w", encoding="utf-8"))
                    print(f"新建檔案...{self.file}")
        
        except Exception as e:
            send.pause(text="建立config時發生錯誤...", e=e)
        

    def read_config(self) -> configparser.ConfigParser:
        """
        檢查config檔案後讀取config並回傳
        """
        try:
            self.check()
            parser_read = configparser.ConfigParser()
            parser_read.read(self.file, encoding="utf-8")
            return parser_read
        except Exception as e:
            send.pause(text="讀取config時發生錯誤...", e=e)
            return None


if __name__ == '__main__':
    # 參數池
    pool = [
        {
            "name":"setting",
            "item":{
                "machine_number":"int",
                "global_setting_path":"str",
                "api_key":"str",
                "user_agent":"str",
                "test":"okok",
            }
        },
    ]

    config = Config(file="heloo.ini", config_pool=pool)
    config.check()
