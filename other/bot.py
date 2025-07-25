from self_packages import kawaii_fox
from setting import settings

def discord_message(all_filter_jobs:dict):
    """
    將篩選後新找到的職缺資料，整理成訊息後逐一送出
    """
    if len(all_filter_jobs) <= 0:
        print(">>沒有需要傳送discord的訊息")
        return -1
    
    bot_message_list = []
    for filter_jobs in all_filter_jobs.values():
        for job in filter_jobs:
            bot_message = f"### {job["更新"]} | [{job["標題"]}](<{job["連結"]}>)\n"
            bot_message += f"```[企業] {job["企業"]}\n"
            bot_message += f"[地區] {job["地區"]}\n"
            bot_message += f"[學歷] {job["學歷"]}\n"
            bot_message += f"[經驗] {job["經驗"]}\n"
            bot_message += f"[薪資] {job["薪資"]}\n"
            bot_message += f"[說明]\n{job["說明"]}```"
            bot_message_list.append(bot_message)

    kawaii_fox.start(api_key=settings.discord_api_key, channel_id=settings.channel_id, message=bot_message_list)