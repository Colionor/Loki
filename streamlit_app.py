import streamlit as st
import csv


def load_events():
    """
    从 CSV 文件中加载事件记录
    :return: 包含所有事件记录的列表，每个记录是一个元组 (日期, 事件描述)
    """
    events = []
    try:
        with open('events.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                events.append((row[0], row[1]))
    except FileNotFoundError:
        pass
    return events


def save_events(events):
    """
    将事件记录保存到 CSV 文件中
    :param events: 包含所有事件记录的列表，每个记录是一个元组 (日期, 事件描述)
    """
    with open('events.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        for date, event in events:
            writer.writerow([date, event])


def add_event(events, date, event):
    """
    向事件列表中添加新事件，并保存到文件
    :param events: 包含所有事件记录的列表，每个记录是一个元组 (日期, 事件描述)
    :param date: 新事件的日期
    :param event: 新事件的描述
    :return: 更新后的事件列表
    """
    date_str = date.strftime('%Y-%m-%d')
    events.append((date_str, event))
    save_events(events)
    return events


def display_events(events):
    """
    在 Streamlit 应用中显示所有事件记录
    :param events: 包含所有事件记录的列表，每个记录是一个元组 (日期, 事件描述)
    """
    st.subheader("大事年表")
    for date, event in events:
        formatted_date = f"{date[:4]}年{date[5:7]}月{date[8:]}日"
        st.write(f"{formatted_date}，{event}")


def main():
    # 应用标题
    st.title("我的大事年表")

    # 加载已有事件
    events = load_events()

    # 添加事件的输入框
    date = st.date_input("日期")
    event = st.text_input("事件描述")
    if st.button("添加事件"):
        events = add_event(events, date, event)

    # 显示所有事件
    display_events(events)


if __name__ == "__main__":
    main()
    