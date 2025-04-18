import streamlit as st
import csv
from datetime import datetime, timedelta
import requests
import base64


# 从 Streamlit Cloud Secret 中获取 GitHub 仓库信息
GITHUB_REPO_OWNER = st.secrets["GITHUB_REPO_OWNER"]
GITHUB_REPO_NAME = st.secrets["GITHUB_REPO_NAME"]
GITHUB_FILE_PATH = st.secrets["GITHUB_FILE_PATH"] 
GITHUB_API_TOKEN = st.secrets["GITHUB_API_TOKEN"]


def load_events():
    events = []
    try:
        url = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/contents/{GITHUB_FILE_PATH}"
        headers = {
            "Authorization": f"token {GITHUB_API_TOKEN}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            content = base64.b64decode(response.json()["content"]).decode("utf-8")
            lines = content.splitlines()
            reader = csv.reader(lines)
            for row in reader:
                events.append((row[0], row[1]))
    except Exception:
        pass
    return events


def save_events(events):
    with open('{GITHUB_FILE_PATH}', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        for date, event in events:
            writer.writerow([date, event])

    # 读取本地文件内容
    with open('{GITHUB_FILE_PATH}', 'r', encoding='utf-8') as file:
        content = file.read()

    # 获取文件的 SHA 值
    url = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/contents/{GITHUB_FILE_PATH}"
    headers = {
        "Authorization": f"token {GITHUB_API_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    sha = response.json().get("sha") if response.status_code == 200 else None

    # 编码内容为 Base64
    encoded_content = base64.b64encode(content.encode("utf-8")).decode("utf-8")

    # 推送更新到 GitHub
    data = {
        "message": "memory update",
        "content": encoded_content
    }
    if sha:
        data["sha"] = sha
    response = requests.put(url, headers=headers, json=data)
    if response.status_code == 200 or response.status_code == 201:
        st.success("记忆接入完毕")
    else:
        st.error("记忆接入失败{response.text}")
        # st.error(response.text)


def add_event(events, date, event):
    date_str = date.strftime('%Y-%m-%d')
    events.append((date_str, event))
    events.sort(key=lambda x: x[0])
    save_events(events)
    return events


def display_events(events):
    # st.subheader("时间线")
    for date, event in events:
        formatted_date = f"{date[:4]}年{date[5:7]}月{date[8:]}日"
        st.write(f"{formatted_date}，{event}")


def main():
    st.title("「生命长河」")
    # 计算 50 年前的日期
    fifty_years_ago = datetime.now() - timedelta(days=365 * 50)
    events = load_events()
    with st.sidebar:
        st.subheader("新的记忆")
        date = st.date_input("那天……", min_value=fifty_years_ago)
        event = st.text_input("发生了……")
        if st.button("接入"):
            events = add_event(events, date, event)
    display_events(events)


if __name__ == "__main__":
    main()
    