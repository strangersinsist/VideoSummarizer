# VideoNoteApp.py

import streamlit as st
import tempfile
import cv2
from PIL import Image
import io
from docx import Document
from docx.shared import Inches
from streamlit_drawable_canvas import st_canvas

class VideoNoteApp:
    def __init__(self):
        self.initialize_session_state()

    def initialize_session_state(self):
        if "snapshots" not in st.session_state:
            st.session_state.snapshots = []
        if "video_file" not in st.session_state:
            st.session_state.video_file = None
        if "edited_image" not in st.session_state:
            st.session_state.edited_image = None
        if "current_frame_pos" not in st.session_state:
            st.session_state.current_frame_pos = 0
        if "canvas_key" not in st.session_state:
            st.session_state.canvas_key = 0
        if "url" not in st.session_state:  
            st.session_state.url = 0

    def add_snapshot(self, image_data, video_time, annotation):
        st.session_state.snapshots.append({"image": image_data, "time": video_time, "annotation": annotation})

    def delete_snapshot(self, index):
        del st.session_state.snapshots[index]

    def update_annotation(self, index, new_annotation):
        st.session_state.snapshots[index]["annotation"] = new_annotation

    def export_to_docx(self):
        doc = Document()
        doc.add_heading('Video Notes', 0)
        for snapshot in st.session_state.snapshots:
            doc.add_picture(io.BytesIO(snapshot["image"]), width=Inches(4))
            doc.add_paragraph(f"Time: {snapshot['time']} seconds")
            doc.add_paragraph(snapshot["annotation"])
            doc.add_paragraph("\n")
        return doc

    def load_video(self):
        st.markdown("## 上传视频文件")
        uploaded_video = st.file_uploader("选择视频文件", type=["mp4", "mov", "avi"])

        if uploaded_video is not None:
            # 保存上传的视频文件
            tfile = tempfile.NamedTemporaryFile(delete=False)
            tfile.write(uploaded_video.read())
            st.session_state.video_file = tfile.name
            
            # 获取视频文件名并提取视频 ID
            video_filename = uploaded_video.name
            video_id = video_filename.split('.')[0]  # 获取文件名，不含后缀
            youtube_url = f"https://www.youtube.com/watch?v={video_id}"
            st.session_state.url = youtube_url  # 保存完整的 YouTube URL

        # 显示上传的视频
        if st.session_state.video_file is not None:
            st.video(st.session_state.video_file)

    def take_notes(self):
        if st.session_state.video_file is not None:
            cap = cv2.VideoCapture(st.session_state.video_file)
            if cap.isOpened():
                st.success("视频加载成功")

                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                fps = int(cap.get(cv2.CAP_PROP_FPS))
                duration = total_frames / fps

                seconds_slider = st.slider("选择视频秒数", 0, int(duration), 0)
                frame_pos = int(seconds_slider * fps)

                if seconds_slider != st.session_state.current_frame_pos / fps:
                    st.session_state.current_frame_pos = frame_pos
                    st.session_state.canvas_key += 1
                    st.session_state.edited_image = None

                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_pos)
                ret, frame = cap.read()

                if ret:
                    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                    st.session_state.edited_image = io.BytesIO()
                    img.save(st.session_state.edited_image, format="PNG")
                    st.session_state.edited_image.seek(0)

                    st.image(img, caption=f"当前帧: {int(seconds_slider)}秒", use_column_width=True)
                    st.markdown(f"**视频时间：{int(seconds_slider)} 秒**")

                    drawing_mode = st.selectbox("选择绘制模式", ("freedraw", "line", "rect", "circle", "transform"))
                    stroke_width = st.slider("笔刷粗细: ", 1, 25, 3)
                    color = st.color_picker("选择颜色: ", "#000000")

                    canvas_result = st_canvas(
                        fill_color="rgba(255, 165, 0, 0.3)",
                        stroke_width=stroke_width,
                        stroke_color=color,
                        background_image=Image.open(st.session_state.edited_image).convert("RGBA") if st.session_state.edited_image else None,
                        update_streamlit=True,
                        height=360,
                        drawing_mode=drawing_mode,
                        key=f"canvas_{st.session_state.canvas_key}",
                    )

                    if canvas_result.image_data is not None:
                        edited_image = Image.fromarray(canvas_result.image_data.astype("uint8"), "RGBA")
                        original_img = Image.open(st.session_state.edited_image).convert("RGBA")

                        if original_img.size != edited_image.size:
                            edited_image = edited_image.resize(original_img.size)

                        combined_image = Image.alpha_composite(original_img, edited_image)

                        img_byte_arr = io.BytesIO()
                        combined_image.save(img_byte_arr, format="PNG")
                        st.session_state.edited_image = img_byte_arr.getvalue()

            annotation = st.text_area("输入批注内容")
            if st.button("添加批注") and st.session_state.edited_image and annotation:
                self.add_snapshot(st.session_state.edited_image, int(seconds_slider), annotation)
                st.success(f"已添加批注: {int(seconds_slider)}秒 - {annotation}")

            self.display_notes()

    def display_notes(self):
        st.markdown("### 已添加的批注")
        with st.container():
            for i, snapshot in enumerate(st.session_state.snapshots):
                with st.expander(f"批注 {i+1}: {snapshot['time']} 秒"):
                    st.image(snapshot["image"], caption=f"{snapshot['time']}秒 - {snapshot['annotation']}")
                    new_annotation = st.text_area(f"编辑批注 {i+1}", value=snapshot["annotation"], key=f"edit_{i}")
                    if st.button("更新批注", key=f"update_{i}"):
                        self.update_annotation(i, new_annotation)
                        st.success("批注已更新")
                    if st.button("删除", key=f"delete_{i}"):
                        self.delete_snapshot(i)
                        st.experimental_rerun()

    def export_notes(self):
        st.markdown("## 导出笔记")
        if st.button("导出为 DOCX"):
            doc = self.export_to_docx()
            buffer = io.BytesIO()
            doc.save(buffer)
            buffer.seek(0)
            st.download_button("下载 DOCX 文件", data=buffer, file_name="video_notes.docx")
