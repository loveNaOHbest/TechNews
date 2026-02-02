import requests
import feedparser
from datetime import datetime, timedelta
import os
import time

def get_tech_news():
    # 使用 IT之家的 RSS 源
    rss_url = "https://www.ithome.com/rss/"
    feed = feedparser.parse(rss_url)
    news_list = []
    now = datetime.utcnow()
    yesterday = now - timedelta(days=1)

    for entry in feed.entries:
        published_time = datetime.fromtimestamp(time.mktime(entry.published_parsed))
        if published_time > yesterday:
            news_list.append(f"- [{entry.title}]({entry.link})")
    return "\n".join(news_list)

def send_to_wechat(content):
    send_key = os.getenv("SERVERCHAN_SENDKEY")
    url = f"https://sctapi.ftqq.com/{send_key}.send"
    data = {
        "title": f"今日科技早报 - {datetime.now().strftime('%Y-%m-%d')}",
        "desp": f"### 过去24小时科技热点：\n\n{content}\n\n> 来源：GitHub Actions"
    }
    requests.post(url, data=data)

if __name__ == "__main__":
    news = get_tech_news()
    if news:
        send_to_wechat(news)
