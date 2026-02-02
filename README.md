# My_News
# 🧩 TechNews: 个人全能兴趣报 

<p align="center">
  <img src="https://img.shields.io/github/actions/workflow/status/loveNaOHbest/TechNews/daily_news.yml?branch=main&style=for-the-badge&logo=githubactions&logoColor=white" alt="Actions Status">
  <img src="https://img.shields.io/github/last-commit/loveNaOHbest/TechNews?style=for-the-badge&logo=git&logoColor=white" alt="Last Commit">
  <img src="https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python Version">
</p>

---

## 📖 项目简介
本项目是一个基于 **GitHub Actions** 的自动化机器人，每天定时抓取我最感兴趣的科技、数码、竞技及生活资讯，并通过 **Server酱** 推送到微信。

### 🌟 核心功能
- 🛰️ **双城天气**：利用高德 API 实时监控 **合肥 & 南京** 的气温、湿度与风力，助力马拉松训练。
- 🚀 **深度资讯**：自动抓取 IT之家、少数派、Linux.do 的 RSS 24h 精选。
- 📺 **圈内热点**：聚合 B站热门、HLTV 战报、5EPlay 以及 NGA 硬核社区。
- 📚 **备考助手**：内置考研倒计时，提醒每天的复习进度。

---

## 🛠️ 运行机制
1. **触发器**：每天北京时间 `08:05` 与 `22:15` 自动执行。
2. **处理层**：Python 脚本解析 API 与 RSS 数据，生成个性化 Markdown 报表。
3. **推送层**：通过 Server酱 SCT 接口发送至个人微信。

---

## 📸 个人装备与爱好
- **相机**: Nikon Z30 📸
- **竞技**: CS2 (HLTV/5E), 王者荣耀, 金铲铲
- **运动**: 马拉松/田径训练 🏃
- **学习**: 2026 考研冲刺中... 📖

---

## 🔧 如何部署
如果你也想搭建一个类似的机器人：
1. Fork 本仓库。
2. 在 `Settings -> Secrets -> Actions` 中配置：
   - `SERVERCHAN_SENDKEY`: 你的 Server酱 SendKey
   - `AMAP_KEY`: 你的高德开放平台 Key
3. 修改 `news_bot.py` 中的城市代码和兴趣链接。

---

<p align="center">
  <i>💡 今天的代码写了吗？别忘了给相机充电。</i>
</p>
