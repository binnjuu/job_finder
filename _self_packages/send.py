from datetime import datetime
import threading
import json
import os
import sys
import traceback


#普通訊息
LOCK = threading.Lock()
def message(message:str):
    with LOCK:
        print(f"\n▲{datetime.today().strftime('%Y-%m-%d %H:%M:%S')}\n{message}")


#提示訊息
def tip_message(message:str):
    with LOCK:
        print(f"\n▲{datetime.today().strftime('%Y-%m-%d %H:%M:%S')}\n[提示訊息]\n{message}")


#錯誤訊息
def error_message(message:str):
    with LOCK:
        print(f"\n▲{datetime.today().strftime('%Y-%m-%d %H:%M:%S')}\n[錯誤訊息]\n{message}")


def pretty(d, indent=4, enable_print=True):
   """
   印出縮排後的dict資料
   """
   text = json.dumps(d, indent=indent, default=str, ensure_ascii=False)
   if enable_print:
      print(text)
   return text


def get_error_info(e) -> str:
    """
    檢查錯誤訊息並回傳
    """
    # source: https://dotblogs.com.tw/caubekimo/2018/09/17/145733
    error_class = e.__class__.__name__ #取得錯誤類型
    try:
        detail = e.args[0] #取得詳細內容
    except:
        detail = "無法取得[detail]訊息"

    cl, exc, tb = sys.exc_info() #取得Call Stack
    lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
    fileName = lastCallStack[0] #取得發生的檔案名稱
    lineNum = lastCallStack[1] #取得發生的行號
    funcName = lastCallStack[2] #取得發生的函數名稱
    errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
    
    return errMsg


def pause(text="測試中...", e="") -> None:
    """
    顯示錯誤訊息，並暫停程式執行
    """
    if type(e) == str:
        print(f"{text}\n{e}\n")
    else:
        errMsg = get_error_info(e=e)
        message = f"{text}\n{errMsg}\n"
        error_message(message)

    input("輸入Enter關閉程式...")
    sys.exit(0)


def color_message(message, message_type):
    """
    印出帶有顏色的訊息
    """
    bcolors = {
        "HEADER": '\033[95m',
        "OKBLUE": '\033[94m',
        "OKCYAN": '\033[96m',
        "OKGREEN": '\033[92m',
        "WARNING": '\033[93m',
        "FAIL": '\033[91m',
        "ENDC": '\033[0m',
        "BOLD": '\033[1m',
        "UNDERLINE" : '\033[4m',
    }

    with LOCK:
        print(f"{bcolors[message_type]}{message}{bcolors["ENDC"]}")
        