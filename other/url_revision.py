import re

def page_number(url:str, arg:str, page=1):
    """
    arg=參數名稱
    修改網址中的頁面參數
    """
    # 在網址中找目前的頁碼
    currently_page_compile = re.compile(rf"{arg}\d*")
    currently_page = currently_page_compile.search(url).group().replace(arg, "")
    
    # 將頁碼調整為指定值
    revision_url = url.replace(f"{arg}{currently_page}", f"{arg}{page}")
    
    return revision_url