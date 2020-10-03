#encoding=utf-8
import requests
import json
async def get_weather(location:str, weather_type="")->str:
    trans_table = trans_tab_import()
    othername=[]
    for v in trans_table.values():
        othername+=v
    location_out = location
    if weather_type == "":
        weather_type = "now"
    if location == "":
        location = "auto_ip"
    
    elif location in othername:
        location = [key for key,value in trans_table.items() if location in value][0]
    url = "https://free-api.heweather.net/s6/weather/{0}?location={1}&key=bcf75a99d9fc40f5bf46b79d1aaeb4df".format(
        weather_type, location)
    print(url)
    res = requests.get(url)
    if res.status_code == 200:
        info = res.json()
        info = info['HeWeather6'][0]
        if info['status']!="unknown location":

            now = info['now']
            msg = """现在由琉璃播报天气情况：
搜索地点：{0}
地点：{10} {11} {12} {13}
更新时间：{1}
天气:{2}  
温度:{3}℃ 体感温度:{4}℃
风向:{5}  风力:{6}级 风速:{7} m/s
湿度:{8}%  大气压强:{9}hPa""".format(
        location_out,
        info['update']['loc'],
        now['cond_txt'],
        now['tmp'],
        now['fl'],
        now['wind_deg'],
        now['wind_sc'],
        now['wind_spd'],
        now['hum'],
        now['pres'],
        info['basic']['cnty'],
        info['basic']['admin_area'],
        info['basic']['parent_city'],
        info['basic']['location']
    )
        else:
            msg="琉璃不知道这是哪里，呜呜呜~~~"
    return msg
def trans_tab_import()->dict:
    with open("plugins/weather/data/location_other_name.json",'r',encoding='utf-8') as f:
        tran_tab=json.load(f)
    return dict(tran_tab)
