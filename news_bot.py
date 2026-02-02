import requests
import feedparser
from datetime import datetime, timedelta
import os
import time

# --- 配置区 ---
# 天气预报城市（用于马拉松训练参考）
CITY = "南京" # 你可以改为洛阳或其他城市

def get_weather():
    """获取天气预报，方便安排跑步"""
    try:
        url = f"https://api.vvhan.com/api/weather?city={CITY}"
        res = requests.get(url).json()
        if res['success']:
            data = res['data']
            return f"🌤️ {CITY}天气：{data['type']} | {data['low']}~{data['high']} | {data['week']}"
    except: return "🌤️ 天气数据获取失败"

def get_hot_lists():
    """获取微博和知乎热榜（使用聚合接口避开反爬）"""
    content = "#### 🔥 实时热搜 (微博 & 知乎)\n"
    try:
        # 微博热搜
        wb_res = requests.get("https://api.vvhan.com/api/hotlist?type=wbHot").json()
        wb_items = [f"- [微博] {i['title']}]({i['url']})" for i in wb_res['data'][:5]]
        # 知乎热榜
        zh_res = requests.get("https://api.vvhan.com/api/hotlist?type=zhihuHot").json()
        zh_items = [f"- [知乎] {i['title']}]({i['url']})" for i in zh_res['data'][:5]]
        return content + "\n".join(wb_items + zh_items)
    except:
        return content + "- 暂时无法连接社交热点接口"

def get_bili_popular():
    """B站热门：覆盖二次元、数码、游戏"""
    try:
        url = "https://api.bilibili.com/x/web-interface/popular?ps=6"
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).json()
        return "#### 📺 B站热门精选\n" + "\n".join([f"- [B站] {i['title']}]({i['short_link_v2']})" for i in res['data']['list']])
    except: return "#### 📺 B站热门\n- 暂时无法获取"

def get_rss_tech():
    """深度科技与摄影 (IT之家 & 少数派)"""
    sources = {"科技深挖": "https://www.ithome.com/rss/", "数码摄影": "https://sspai.com/feed"}
    news = []
    now = datetime.utcnow()
    for name, url in sources.items():
        try:
            f = feedparser.parse(url)
            for e in f.entries[:5]:
                news.append(f"- 【{name}】[{e.title}]({e.link})")
        except: continue
    return "#### 🚀 深度科技资讯\n" + ("\n".join(news) or "- 暂无更新")

def generate_report():
    # 考研倒计时逻辑（假设2027考研初试为2026年12月20日）
    exam_date = datetime(2026, 12, 20)
    now_bj = datetime.utcnow() + timedelta(hours=8)
    countdown = (exam_date - now_bj).days
    
    report = f"### 🧩 您的全能早晚报 | {now_bj.strftime('%H:%M')}\n"
    report += f"> 📅 考研倒计时：{countdown} 天 | {get_weather()}\n\n"
    
    report += get_hot_lists() + "\n\n"
    report += get_rss_tech() + "\n\n"
    report += get_bili_popular() + "\n\n"
    
    report += "#### 🎮 垂直兴趣直达\n"
    report += "- [HLTV] [CS2 赛事中心](https://www.hltv.org/)\n"
    report += "- [王者荣耀] [官网公告更新](https://pvp.qq.com/)\n"
    report += "- [考研] [中国研究生招生信息网](https://yz.chsi.com.cn/)\n\n"
    
    report += "--- \n> 💡 今天的代码写了吗？别忘了给 Nikon Z30 充电！📸"
    return report

def send_to_wechat(content):
    send_key = os.getenv("SERVERCHAN_SENDKEY")
    url = f"https://sctapi.ftqq.com/{send_key}.send"
    requests.post(url, data={"title": "您的全能兴趣报已送达", "desp": content})

if __name__ == "__main__":
    send_to_wechat(generate_report())
