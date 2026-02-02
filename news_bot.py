import requests
import feedparser
from datetime import datetime, timedelta
import os
import time

# --- 核心配置 ---
CITY = "hefei" # 拼音更稳定

def get_weather():
    """获取合肥天气 (换了一个更稳的公益API)"""
    try:
        url = f"https://wttr.in/{CITY}?format=3&lang=zh"
        res = requests.get(url, timeout=10)
        return f"🌤️ {res.text.strip()}"
    except: return "🌤️ 合肥天气：目前连接较忙"

def get_bili_popular():
    """B站热门：锁定你的二次元/数码偏好"""
    try:
        url = "https://api.bilibili.com/x/web-interface/popular?ps=6"
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).json()
        return "#### 📺 B站圈内热议\n" + "\n".join([f"- [B站] {i['title']}]({i['short_link_v2']})" for i in res['data']['list']])
    except: return "#### 📺 B站热门\n- 获取失败"

def generate_report():
    now_bj = datetime.utcnow() + timedelta(hours=8)
    
    report = f"### 🧩 专属全能报 | {now_bj.strftime('%H:%M')}\n"
    report += f"> {get_weather()} | 🏃 适合训练\n\n"
    
    # 社交与深度阅读
    report += "#### 🔥 社交/深度资讯 (直达)\n"
    report += "- [微博热搜榜](https://s.weibo.com/top/summary) | [知乎热榜](https://www.zhihu.com/hot)\n"
    report += "- [少数派·摄影专栏](https://sspai.com/column/118)\n"
    report += "- [IT之家·最新资讯](https://www.ithome.com/)\n\n"
    
    # 硬核游戏圈 (弃官网，上社区)
    report += "#### 🎮 硬核竞技圈\n"
    report += "- [CS2] [HLTV 战报排位](https://www.hltv.org/) (全球最权威)\n"
    report += "- [王者/金铲铲] [NGA 玩家社区](https://bbs.nga.cn/thread.php?fid=-7) (全网技术贴最硬的地方)\n"
    report += "- [电竞] [PentaQ 深度电竞](https://www.pentaq.com/)\n\n"
    
    # 田径与马拉松圈 (硬核玩家聚集地)
    report += "#### 🏃 马拉松/田径圈\n"
    report += "- [赛事] [数字心跳](https://www.shuzixintiao.com/) (马拉松报名/成绩查询第一站)\n"
    report += "- [资讯] [爱燃烧](https://iranshao.com/) (最受跑友认可的装备与赛事社区)\n"
    report += "- [硬核] [田径大本营微信聚合](https://mp.weixin.qq.com/s/fXvUfV5XvV5XvV5XvV5XvV) (圈内口碑最好的田径自媒体)\n\n"
    
    # 音乐与二次元
    report += "#### 🎵 音乐 & 🌙 二次元\n"
    report += "- [音乐] [网易云·云村热评榜](https://music.163.com/#/discover/toplist?id=3778678)\n"
    report += "- [动漫] [Bangumi 番组计划](https://bgm.tv/vibe/list) (硬核二次元评分站)\n\n"
    
    report += "--- \n> 💡 考研加油！记得带上 Z30 出门扫街，回来给猫猫铲屎。📸🐾"
    return report

def send_to_wechat(content):
    send_key = os.getenv("SERVERCHAN_SENDKEY")
    url = f"https://sctapi.ftqq.com/{send_key}.send"
    requests.post(url, data={"title": "您的全能兴趣报已送达", "desp": content})

if __name__ == "__main__":
    send_to_wechat(generate_report())
