import streamlit as st
from VideoNoteApp import VideoNoteApp
from VideoSummaryApp import VideoSummaryApp

def main():
    # 设置页面布局
    st.set_page_config(layout="wide")
    st.title("AI Vedio Summary WebApp")

    # 实例化两个应用
    note_app = VideoNoteApp()
    summary_app = VideoSummaryApp()

    # 创建左右列布局
    left_column, right_column = st.columns([3, 2])

    # 左栏：视频加载和总结生成
    with left_column:

        note_app.load_video()

        summary_app.load_session_state() 

        # 生成 Transcript
        if st.button("Generate Transcript"):
            summary_app.generate_transcript()
        summary_app.display_transcript()

        # 生成 Summary
        if st.button("Generate Summary"):
            summary_app.generate_summary()
        summary_app.display_summary()

        # 生成带时间戳的内容
        if st.button("Generate Timestamped Content"):
            summary_app.generate_time_stamps()
        summary_app.display_time_stamps()

        # 生成词云
        if st.button("Generate WordCloud"):
            summary_app.generate_wordcloud(width=800, height=400)    
        summary_app.display_wordcloud(figsize=(5, 3))

        #生成思维导图
        if st.button("Generate Mindmap"):
            summary_app.generate_mindmap()
        summary_app.display_mindmap()

    # 右栏：笔记功能
    with right_column:
        st.markdown("## Take notes")
        note_app.take_notes()
        note_app.export_notes()

if __name__ == "__main__":
    main()
