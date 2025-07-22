from today_json import Today_Json


def json_file(job:dict):
    """
    檢查某個職缺資料的連結是否已經在輸出的json檔案中
    """
    today_json = Today_Json()
    json_contents = today_json.read()
    if json_contents == -1:
        return False
    
    all_links = []
    for site_data in dict(json_contents).values():
        for data in site_data:
            all_links.append(data["連結"])

    if job["連結"] in all_links:
        # print("存在")
        return True
    else:
        # print("不存在")
        return False