import requests
import feedparser
from datetime import datetime, timedelta
import os
import time

# --- 配置区 ---
# IT之家, 少数派, 36氪, Linux.do 等 RSS 源
RSS_SOURCES = {
    "科技深挖": "https://www.ithome.com/rss/",
    "数码生活": "https://sspai.com/feed",
}

def get_rss_news():
    """保留原有逻辑：抓取过去24小时的深度科技讯息"""
    news_list = []
    now = datetime.utcnow()
    yesterday = now - timedelta(days=1)
    
    for name, url in RSS_SOURCES.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:8]: # 每个源取前8条
                pub_time = datetime.fromtimestamp(time.mktime(entry.published_parsed))
                if pub_time > yesterday:
                    news_list.append(f"- 【{name}】[{entry.title}]({entry.link})")
        except:
            continue
    return "\n".join(news_list)

def get_bilibili_hot():
    """B站热门：涵盖二次元、数码、游戏"""
    try:
        url = "https://api.bilibili.com/x/web-interface/popular?ps=6"
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).json()
        return "\n".join([f"- [B站热门: {i['title']}]({i['short_link_v2']})" for i in res['data']['list']])
    except: return "- 暂未获取到B站动态"

def get_weibo_hot():
    """微博热搜：社会/娱乐热点"""
    try:
        res = requests.get("https://weibo.com/ajax/side/hotSearch").json()
        return "\n".join([f"- [微博热搜: {i['word']}](https://s.weibo.com/weibo?q={i['word']})" for i in res['data']['realtime'][:8]])
    except: return "- 暂未获取到微博热搜"

def generate_report():
    now_bj = datetime.utcnow() + timedelta(hours=8)
    # 针对你的爱好定制化标签
    hobbies = "📸摄影 | 💻代码 | 🎮CS/王者 | 🏃马拉松 | 📚考研必胜"
    
    report = f"### 🌟 {hobbies}\n\n"
    report += f"**生成时间：{now_bj.strftime('%Y-%m-%d %H:%M')}**\n\n"
    
    report += "#### 🚀 24h 科技精选 (RSS)\n"
    report += (get_rss_news() or "- 暂无更新") + "\n\n"
    
    report += "#### 🔥 社交/深度热议 (微博&知乎)\n"
    report += get_weibo_hot() + "\n\n"
    
    report += "#### 📺 哔哩哔哩热门 (二次元/数码)\n"
    report += get_bilibili_hot() + "\n\n"
    
    report += "--- \n> 💡 考研加油！别忘了带上水壶去跑步。🐾"
    return report

def send_to_wechat(content):
    send_key = os.getenv("SERVERCHAN_SENDKEY")
    url = f"https://sctapi.ftqq.com/{send_key}.send"
    data = {"title": f"今日全能兴趣报", "desp": content}
    requests.post(url, data=data)

if __name__ == "__main__":
    send_to_wechat(generate_report())
