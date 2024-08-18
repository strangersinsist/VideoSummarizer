import streamlit as st
from VideoNoteApp import VideoNoteApp
from VideoSummaryApp import VideoSummaryApp

def main():
    # 设置页面布局
    st.set_page_config(layout="wide")
    st.title("AI 视频总结 WebApp")

    # 实例化两个应用
    note_app = VideoNoteApp()
    summary_app = VideoSummaryApp()

    # 创建左右列布局
    left_column, right_column = st.columns([3, 2])

    # 左栏：视频加载和总结生成
    with left_column:

        note_app.load_video()

        summary_app.load_session_state() 

        # 按钮生成 Transcript
        if st.button("Generate Transcript"):
            summary_app.generate_transcript()

        # 显示 Transcript
        summary_app.display_transcript()

        # 按钮生成 Summary
        if st.button("Generate Summary"):
            summary_app.generate_summary()

        # 显示 Summary
        summary_app.display_summary()

        # 按钮生成带时间戳的内容
        if st.button("Generate Timestamped Content"):
            summary_app.generate_time_stamps()

        # 显示带时间戳的内容
        summary_app.display_time_stamps()

    # 右栏：笔记功能
    with right_column:
        st.markdown("## 做笔记")
        note_app.take_notes()
        note_app.export_notes()

if __name__ == "__main__":
    main()
