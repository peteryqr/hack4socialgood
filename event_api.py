"""Retrieving infromation from web scraping"""
import requests
from bs4 import BeautifulSoup

# 目标URL
url = "https://bookings.lib.msu.edu/calendar/events/?cid=3079&t=g&d=0000-00-00&cal=3079&inc=0"
headers = {"User-Agent": "Mozilla/5.0"}

# 使用 certifi 路径
try:
    response = requests.get(url, headers=headers, verify=certifi.where())
    print("成功获取数据")
    print(response.text)
except requests.exceptions.SSLError as e:
    print(f"SSL 验证失败: {e}")
    # 尝试跳过验证
    response = requests.get(url, headers=headers, verify=False)
    print("跳过验证获取的数据：")
    print(response.text)



html_content = response.text

# 使用 BeautifulSoup 解析 HTML
soup = BeautifulSoup(html_content, "html.parser")

# 存储提取的信息
event_data = []

# 查找所有活动面板
event_panels = soup.find_all("div", class_="panel panel-default track")

for panel in event_panels:
    # 提取活动名称
    name_tag = panel.find("h3", class_="panel-title")
    event_name = name_tag.text.strip() if name_tag else "No Title"

    # 提取活动日期
    date_tag = panel.find("div", class_="date-header")
    event_date = date_tag.text.strip() if date_tag else "No Date"

    # 提取活动描述
    description_tag = panel.find("div", class_="description")
    description = description_tag.text.strip() if description_tag else "No Description"

    # 提取注册链接
    link_tag = panel.find("a", class_="pull-right btn btn-default")
    registration_link = link_tag['href'] if link_tag else "No Link"

    # 存储为字典
    event_data.append({
        "Event Name": event_name,
        "Date": event_date,
        "Description": description,
        "Registration Link": f"https://sessions.studentlife.umich.edu{registration_link}"
    })

# 转换为 DataFrame
events_df = pd.DataFrame(event_data)

# 显示结果
import ace_tools as tools; tools.display_dataframe_to_user(name="Event Details", dataframe=events_df)
