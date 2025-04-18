import streamlit as st
import pandas as pd
from github import Github
import os

# 配置 GitHub 凭证（在Streamlit Cloud环境变量设置）
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # 个人访问令牌
REPO_NAME = "life-timeline"
FILE_NAME = "timeline.csv"

def get_github_repo():
    g = Github(GITHUB_TOKEN)
    return g.get_user().get_repo(REPO_NAME)

def load_data():
    try:
        repo = get_github_repo()
        file = repo.get_contents(FILE_NAME)
        content = file.decoded_content.decode("utf-8")
        return pd.read_csv(pd.compat.StringIO(content))
    except:
        return pd.DataFrame(columns=["date", "title", "detail", "category"])

def save_to_github(df):
    repo = get_github_repo()
    csv_content = df.to_csv(index=False)
    repo.update_file(FILE_NAME, "Update timeline", csv_content, branch="main")

def main():
    st.title("「生命长河」")
    
    # 加载数据
    df = load_data()
    
    # 添加事件
    with st.form("add_event"):
        date = st.date_input("日期")
        title = st.text_input("标题")
        detail = st.text_area("详情")
        category = st.selectbox("分类", ["生活", "工作", "学习"])
        
        if st.form_submit_button("保存"):
            new_row = pd.DataFrame([[date.strftime("%Y-%m-%d"), title, detail, category]])
            df = pd.concat([df, new_row], ignore_index=True)
            save_to_github(df)
            st.success("事件已记录。")

    # 显示时间线
    st.subheader("我的时间线")
    for index, row in df.iterrows():
        with st.expander(f"{row['date']} - {row['title']}"):
            st.write(f"**分类**: {row['category']}")
            st.write(row['detail'])

if __name__ == "__main__":
    main()