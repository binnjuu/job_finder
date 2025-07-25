import sys
from io import StringIO
import datetime
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import time

# 開始執行
def start(api_key:str, channel_id:int, message, at_user_id:str|None = None):
    """
    向discord指定頻道發送一則訊息,
    api_key: 機器人api key,
    channel_id: 指定頻道id，需要是整數型態,
    message: 要送出的訊息(可以是list，會依序送出),

    [可選]at_user_id: 標記一位使用者id
    """
    #client 是我們與 Discord 連結的橋樑，intents 是我們要求的權限
    intents=discord.Intents.default()
    intents.message_content = True
    help_command = commands.DefaultHelpCommand(no_category = '指令清單')
    client = commands.Bot(command_prefix="!", intents=intents, )

    @client.event
    #當機器人完成啟動時
    async def on_ready():
        print('目前登入身份：', client.user)
        #遊玩狀態更改
        game = discord.Game("I'm not a Cat!")
        await client.change_presence(status=discord.Status.idle, activity=game)

        file_date = datetime.datetime.now().strftime(r"%Y-%m-%d %H:%M:%S")
        #發送訊息到特定頻道
        channel = client.get_channel(channel_id)
        # 如果訊息為list格式，則每隔x秒送出一個
        if type(message) is list:
            for msg in message:
                if len(msg) > 2000:
                    buffer = StringIO(msg)
                    file_date = datetime.datetime.now().strftime(r"%Y-%m-%d")
                    f = discord.File(buffer, filename=f"{file_date}.txt")
                    await channel.send(file=f)
                else:
                    output_text = f"`[{file_date}]`"
                    if at_user_id is not None:
                        output_text += f"\n>> <@{at_user_id}> {msg}"
                    else:
                        output_text += f"\n{msg}\n---"

                    await channel.send(output_text)
                time.sleep(1)

        elif len(message) > 2000:
                buffer = StringIO(message)
                file_date = datetime.datetime.now().strftime(r"%Y-%m-%d")
                f = discord.File(buffer, filename=f"{file_date}.txt")
                await channel.send(file=f)
        else:
            output_text = f"`[{file_date}]`"
            if at_user_id is not None:
                output_text += f"\n>> <@{at_user_id}> {message}"
            else:
                output_text += f"\n>> {message}\n---"

            await channel.send(output_text)
  
        #關閉機器人
        await client.close()

    client.run(api_key)