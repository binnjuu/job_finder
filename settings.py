from config import Config
import config_pool

config = Config(file="config.ini", config_pool=config_pool.setting, dir_path="setting").read_config()
driver_port = config.getint(section="setting", option="driver_port")
driver_path = config.get(section="setting", option="driver_path")
profile_save_path = config.get(section="setting", option="profile_save_path")
forld_name = config.get(section="setting", option="forld_name")

discord_api_key = config.get(section="setting", option="discord_api_key")
channel_id = config.getint(section="setting", option="channel_id")

url = {
    "104": config.get(section="setting", option="search_url_104"),
    "1111": config.get(section="setting", option="search_url_1111"),
    "518": config.get(section="setting", option="search_url_518"),
    # "taiwanjobs": config.get(section="setting", option="search_url_taiwanjobs"),
}