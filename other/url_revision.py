import re

def page_number(url:str, page=1):
    """
    修改網址中的page=參數
    """
    # 在網址中找目前的頁碼
    currently_page_compile = re.compile(r"page=\d*")
    currently_page = currently_page_compile.search(url).group().replace("page=", "")
    
    # 將頁碼調整為指定值
    revision_url = url.replace(f"page={currently_page}", f"page={page}")
    
    return revision_url