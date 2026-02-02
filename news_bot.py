import requests
import feedparser
from datetime import datetime, timedelta
import os
import time

# --- 城市代码配置 ---
CITIES = {"合肥": "340100", "南京": "320100"}

def get_amap_weather():
    """使用高德 API 获取详细的双城天气"""
    # 从 Github Secrets 读取 Key
    amap_key = os.getenv("AMAP_KEY")
    if not amap_key:
        return "🌤️ 天气 Key 未配置"
    
    weather_reports = []
    for city_name, city_code in CITIES.items():
        try:
            url = f"https://restapi.amap.com/v3/weather/weatherInfo?city={city_code}&key={amap_key}&extensions=base"
            res = requests.get(url, timeout=10).json()
            if res['status'] == '1' and res['lives']:
                d = res['lives'][0]
                # 针对马拉松训练，增加了湿度和风力展示
                weather_reports.append(f"{city_name}：{d['weather']} {d['temperature']}°C | {d['winddirection']}风{d['windpower']}级 | 湿度{d['humidity']}%")
        except:
            continue
    return " | ".join(weather_reports)

def get_rss_news():
    """抓取过去24小时深度资讯 (IT之家/少数派/Linux.do)"""
    sources = {
        "科技深挖": "https://www.ithome.com/rss/",
        "数码摄影": "https://sspai.com/feed",
        "开源圈子": "https://linux.do/latest.rss"
    }
    news = []
    now = datetime.utcnow()
    yesterday = now - timedelta(days=1)
    
    for name, url in sources.items():
        try:
            feed = feedparser.parse(url)
            for e in feed.entries[:5]:
                try:
                    pub_time = datetime.fromtimestamp(time.mktime(e.published_parsed))
                except: pub_time = now
                if pub_time > yesterday:
                    news.append(f"- 【{name}】[{e.title}]({e.link})")
        except: continue
    return "\n".join(news)

def generate_report():
    # 考研倒计时 (基于 2026/12/20)
    exam_date = datetime(2026, 12, 20)
    now_bj = datetime.utcnow() + timedelta(hours=8)
    countdown = (exam_date - now_bj).days
    
    report = f"### 🧩 全能兴趣报 | {now_bj.strftime('%H:%M')}\n"
    report += f"> 📅 考研倒计时：{countdown} 天\n"
    report += f"> 🌤️ {get_amap_weather()}\n\n"
    
# 1. 社交热点 (直达链接)
    report += "#### 🔥 社交实时热点 (直达)\n- [微博热搜榜](https://s.weibo.com/top/summary) | [知乎热榜](https://www.zhihu.com/hot)\n\n"
    
    # 2. 深度资讯
    report += "#### 🚀 24h 深度科技/摄影/开源 (RSS)\n" + (get_rss_news() or "- 暂无更新") + "\n\n"
    
    # 3. 硬核玩家圈 & 马拉松 (你的圈内偏好)
    report += "#### 🎮 硬核竞技 & 🏃 跑者空间\n"

    # CS2 模块
    report += "- [CS2-HLTV 战报](https://www.hltv.org/)\n"
    report += "- [CS2-5E 战报](https://event.5eplay.com/csgo/matches/)\n"
    # 音乐与社区
    report += "- [网易云热歌](https://music.163.com/#/discover/toplist?id=3778678)\n"
    report += "- [NGA 硬核社区](https://bbs.nga.cn/thread.php?fid=-7)\n"
    # 跑步模块 (移除了B站复杂的追踪参数)
    report += "- [数字心动赛事](https://race.shuzixindong.com/)\n"
    report += "- [马拉圈动态](https://space.bilibili.com/1949143691)\n\n"
    
    report += "--- \n> 💡 考研加油！别忘了给 Nikon Z30 充电。📸"
    return report

def send_to_wechat(content):
    send_key = os.getenv("SERVERCHAN_SENDKEY")
    requests.post(f"https://sctapi.ftqq.com/{send_key}.send", data={"title": "您的专属兴趣报", "desp": content})

if __name__ == "__main__":
    send_to_wechat(generate_report())
