import requests
import feedparser
from datetime import datetime, timedelta
import os
import time

# --- 配置区 ---
CITY = "合肥" 

def get_weather():
    """获取合肥天气，助力马拉松训练"""
    try:
        url = f"https://api.vvhan.com/api/weather?city={CITY}"
        res = requests.get(url).json()
        if res['success']:
            data = res['data']
            return f"🌤️ {CITY}天气：{data['type']} | {data['low']}~{data['high']} | {data['tip']}"
    except: return "🌤️ 天气数据获取失败"

def get_bili_popular():
    """B站热门：涵盖二次元、数码、游戏、音乐视频"""
    try:
        url = "https://api.bilibili.com/x/web-interface/popular?ps=6"
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).json()
        return "#### 📺 B站热门 (二次元/数码/游戏)\n" + "\n".join([f"- [B站] {i['title']}]({i['short_link_v2']})" for i in res['data']['list']])
    except: return "#### 📺 B站热门\n- 暂时无法获取"

def get_rss_tech():
    """深度科技、摄影与代码开源"""
    sources = {
        "科技深挖": "https://www.ithome.com/rss/", 
        "数码摄影": "https://sspai.com/feed",
        "开源圈": "https://linux.do/latest.rss"
    }
    news = []
    now = datetime.utcnow()
    for name, url in sources.items():
        try:
            f = feedparser.parse(url)
            for e in f.entries[:4]:
                news.append(f"- 【{name}】[{e.title}]({e.link})")
        except: continue
    return "#### 🚀 深度科技/摄影/开源\n" + ("\n".join(news) or "- 暂无更新")

def generate_report():
    # 考研倒计时逻辑
    exam_date = datetime(2026, 12, 20)
    now_bj = datetime.utcnow() + timedelta(hours=8)
    countdown = (exam_date - now_bj).days
    
    report = f"### 🧩 专属全能报 | {now_bj.strftime('%H:%M')}\n"
    report += f"> 📅 考研倒计时：{countdown} 天 | {get_weather()}\n\n"
    
    # 社交直达链接
    report += "#### 🔥 社交实时热点 (直达)\n"
    report += "- [微博热搜榜](https://s.weibo.com/top/summary)\n"
    report += "- [知乎热榜](https://www.zhihu.com/hot)\n\n"
    
    report += get_rss_tech() + "\n\n"
    report += get_bili_popular() + "\n\n"
    
    # 音乐与游戏赛事
    report += "#### 🎵 音乐 & 🎮 游戏竞技\n"
    report += "- [音乐] [网易云热歌榜](https://music.163.com/#/discover/toplist?id=3778678)\n"
    report += "- [CS2] [HLTV 赛事中心](https://www.hltv.org/)\n"
    report += "- [王者/金铲铲] [营地最新动态](https://pvp.qq.com/)\n\n"
    
    # 马拉松与备考
    report += "#### 🏃 马拉松 & 📚 备考空间\n"
    report += "- [马拉松] [中国马拉松赛事日历](http://www.runchina.org.cn/)\n"
    report += "- [田径] [田径大本营动态](https://www.sport.gov.cn/)\n"
    report += "- [考研] [中国研招网](https://yz.chsi.com.cn/)\n\n"
    
    report += "--- \n> 💡 今天的代码写了吗？别忘了给 Nikon Z30 充电，给猫猫铲屎！📸🐾"
    return report

def send_to_wechat(content):
    send_key = os.getenv("SERVERCHAN_SENDKEY")
    url = f"https://sctapi.ftqq.com/{send_key}.send"
    requests.post(url, data={"title": "您的全能兴趣报已送达", "desp": content})

if __name__ == "__main__":
    send_to_wechat(generate_report())
