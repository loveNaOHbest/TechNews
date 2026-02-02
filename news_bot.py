import requests
import feedparser
from datetime import datetime, timedelta
import os
import time

# --- 配置区 ---
CITY = "hefei" # 合肥

def get_weather():
    """获取合肥天气 (强制摄氏度单位)"""
    try:
        # 添加 m 参数强制使用公制单位（摄氏度），添加 1 参数只显示简短结果
        url = f"https://wttr.in/{CITY}?format=%c+%t+%w&m&lang=zh"
        res = requests.get(url, timeout=10)
        # 结果会显示类似：☀️ +10°C ↗️11km/h
        return f"🌤️ 合肥今日：{res.text.strip()}"
    except: 
        return "🌤️ 合肥天气：获取中..."

def get_rss_news():
    """保留你满意的 RSS 抓取逻辑：IT之家、少数派、Linux.do"""
    sources = {
        "科技深挖": "https://www.ithome.com/rss/",
        "数码摄影": "https://sspai.com/feed",
        "开源圈子": "https://linux.do/latest.rss"
    }
    news_list = []
    now = datetime.utcnow()
    yesterday = now - timedelta(days=1)
    
    for name, url in sources.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:5]: # 每个源取前5条
                # 解析时间
                try:
                    pub_time = datetime.fromtimestamp(time.mktime(entry.published_parsed))
                except:
                    pub_time = now # 兜底
                if pub_time > yesterday:
                    news_list.append(f"- 【{name}】[{entry.title}]({entry.link})")
        except:
            continue
    return "\n".join(news_list)

def get_bilibili_hot():
    """保留 B站热门"""
    try:
        url = "https://api.bilibili.com/x/web-interface/popular?ps=6"
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).json()
        return "\n".join([f"- [B站] {i['title']}]({i['short_link_v2']})" for i in res['data']['list']])
    except: return "- 暂未获取到B站动态"

def generate_report():
    # 保留考研倒计时 (假设2027考研初试为2026年12月20日)
    exam_date = datetime(2026, 12, 20)
    now_bj = datetime.utcnow() + timedelta(hours=8)
    countdown = (exam_date - now_bj).days
    
    report = f"### 🧩 专属全能报 | {now_bj.strftime('%H:%M')}\n"
    report += f"> 📅 考研倒计时：{countdown} 天 | {get_weather()}\n\n"
    
    # 1. 社交热点 (采用直达链接，百分百成功)
    report += "#### 🔥 社交实时热点 (直达)\n"
    report += "- [微博热搜榜](https://s.weibo.com/top/summary) | [知乎热榜](https://www.zhihu.com/hot)\n\n"
    
    # 2. 深度资讯 (保留你喜欢的 RSS 抓取)
    report += "#### 🚀 24h 深度科技/摄影/开源 (RSS)\n"
    report += (get_rss_news() or "- 过去24小时暂无深度更新") + "\n\n"
    
    # 3. B站热门
    report += "#### 📺 哔哩哔哩热门\n"
    report += get_bilibili_hot() + "\n\n"
    
    # 4. 硬核玩家圈 (根据反馈更新为圈内社区)
    report += "#### 🎮 硬核竞技圈 (NGA/HLTV)\n"
    report += "- [CS2] [HLTV 战报排位](https://www.hltv.org/) (全球权威)\n"
    report += "- [王者/金铲铲] [NGA 玩家社区](https://bbs.nga.cn/thread.php?fid=-7) (硬核技术讨论)\n\n"
    
    # 5. 马拉松/田径/音乐
    report += "#### 🏃 跑者与音乐空间\n"
    report += "- [赛事] [数字心跳](https://www.shuzixintiao.com/) (报名/成绩查询)\n"
    report += "- [圈子] [爱燃烧](https://iranshao.com/) (装备与赛事社区)\n"
    report += "- [音乐] [网易云·云村热评榜](https://music.163.com/#/discover/toplist?id=3778678)\n\n"
    
    report += "--- \n> 💡 考研加油！别忘了给 Nikon Z30 充好电。📸"
    return report

def send_to_wechat(content):
    send_key = os.getenv("SERVERCHAN_SENDKEY")
    url = f"https://sctapi.ftqq.com/{send_key}.send"
    requests.post(url, data={"title": "您的全能兴趣报已送达", "desp": content})

if __name__ == "__main__":
    send_to_wechat(generate_report())
