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


def next_page(jobs_list:list, date:str):
    """
    根據傳入資料來判斷是否還需要載入下一頁
    """
    status = True
    # 如果資料抓取失敗或是沒有資料則中斷
    if len(jobs_list) <= 0:
        print("資料抓取失敗或是沒有資料")
        status = False
    # 如果最後一筆資料不是當天的則中斷
    elif jobs_list[-1]["更新"] != date:
        print("最後一筆資料不是當天的")
        status = False
    # 如果最後一筆資料已經儲存在json檔案中則中斷
    elif json_file(jobs_list[-1]):
        print("最後一筆資料已經儲存在json檔案")
        status = False
    
    return status