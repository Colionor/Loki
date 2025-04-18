import streamlit as st
import csv
from datetime import datetime, timedelta


def load_events():
    events = []
    try:
        with open('loki.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                events.append((row[0], row[1]))
    except FileNotFoundError:
        pass
    return events


def save_events(events):
    with open('loki.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        for date, event in events:
            writer.writerow([date, event])


def add_event(events, date, event):
    date_str = date.strftime('%Y-%m-%d')
    events.append((date_str, event))
    events.sort(key=lambda x: x[0])
    save_events(events)
    return events


def display_events(events):
    st.subheader("时间线")
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
        if st.button("记忆"):
            events = add_event(events, date, event)
    display_events(events)


if __name__ == "__main__":
    main()
    