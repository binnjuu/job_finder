## 用途
定時爬取當天的部分台灣求職網站的資料，並於整理後傳送Discord訊息至指定頻道。
<br>
例如104、1111、518、台灣就業通(目前不可用)

![image](https://github.com/binnjuu/job_finder/blob/main/example.gif)


## 前置
### 下載儲存庫
```
git clone https://github.com/binnjuu/job_finder.git
```

### 下載chrome driver
到[Chrome Driver](https://googlechromelabs.github.io/chrome-for-testing/)下載對應版本的Stable chromedriver
<br>
下載完成後解壓縮chromedriver.exe

### Discord Bot API
你需要自行申請一個Discord bot API

### 使用
#### 初次/單次執行
1. 使用CMD或PowerShell開啟專案資料夾
2. 輸入py run.py或是python run.py
3. 依據程式要求設定參數(只有參數還未設定時需要)
4. 等待程式執行結束

#### 定時執行(必須先完成一次上面的步驟)
1. 使用CMD或PowerShell開啟專案資料夾
2. 輸入py main.py或是python main.py
3. 等待程式開始執行(每個小時30分時會執行一次，例如01:30、02:30、03:30...等)

### 其他事項
* 搜尋頁面網址指的是各網站設定好地區與篩選條件的頁面網址
* 搜尋頁面網址中不可以有ASCII Code，例如%2C
* 後續想更改設定可以去修改config.ini
