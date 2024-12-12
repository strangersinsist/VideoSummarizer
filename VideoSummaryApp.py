# VideoSummaryApp.py

import streamlit as st
from model import Model
from prompt import Prompt
from method import Method
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components

class VideoSummaryApp:
    def __init__(self):
        self.video_transcript = ""
        self.summary = ""
        self.video_transcript_time = ""
        self.time_stamps = ""
        self.wordcloud =""
        self.mindmap =""

    def load_session_state(self):
        """Load session state variables."""
        # if "url" not in st.session_state:
        #     st.session_state.url = ""
        if "transcript" not in st.session_state:
            st.session_state.transcript = ""
        if "summary" not in st.session_state:
            st.session_state.summary = ""
        if "time_stamps" not in st.session_state:
            st.session_state.time_stamps = ""
        if "wordcloud" not in st.session_state:
            st.session_state.wordcloud = ""
        if "mindmap" not in st.session_state:
            st.session_state.mindmap = ""

    
    def generate_transcript(self):
        """Generate transcript and update session state."""
        if st.session_state.url:
            transcript = Method.transcript(st.session_state.url)
            st.session_state.transcript = transcript
        return st.session_state.transcript

    def generate_summary(self):
        """Generate summary using the transcript and update session state."""
        self.video_transcript = st.session_state.transcript
        if not self.video_transcript:
            st.warning("Please generate the transcript first.")
            return
        
        self.summary = Model.openai_chatgpt(transcript=self.video_transcript, prompt=Prompt.prompt1())
        st.session_state.summary = self.summary
        return self.summary

    def generate_time_stamps(self):
        """Generate timestamps and update session state."""
        video_id = Method.Id(st.session_state.url)
        self.video_transcript_time = Method.transcript_time(st.session_state.url)
        youtube_url_full = f"https://youtube.com/watch?v={video_id}"
        
        if not self.video_transcript_time:
            st.warning("Please generate the transcript with timestamps first.")
            return
        
        self.time_stamps = Model.openai_chatgpt(
            transcript=self.video_transcript_time,
            prompt=Prompt.prompt1(ID='timestamp'),
            extra=youtube_url_full
        )
        
        st.session_state.time_stamps = self.time_stamps
        return self.time_stamps
    
    def generate_wordcloud(self, width=800, height=400):
        """Generate a word cloud using the transcript and update session state."""
        self.video_transcript = st.session_state.transcript
        if not self.video_transcript:
            st.warning("Please generate the transcript first.")
            return
        
        # 调用 openai 接口生成词云数据
        wordcloud_text = Model.openai_chatgpt(transcript=self.video_transcript, prompt=Prompt.prompt1(ID='wordcloud'))
        
        # 处理生成的文本数据
        words = wordcloud_text.replace(',', ' ')
        
        # 生成词云
        self.wordcloud = WordCloud(width=width, height=height, background_color='white').generate(words)
        st.session_state.wordcloud = self.wordcloud
        return self.wordcloud
    
    def generate_mindmap(self):
        """Generate mindmap using the transcript and update session state."""
        self.video_transcript = st.session_state.transcript
        if not self.video_transcript:
            st.warning("Please generate the transcript first.")
            return
        
        self.mindmap = Model.openai_chatgpt(
            transcript=self.video_transcript, 
            prompt=Prompt.prompt1(ID='mindmap')
        )
        st.session_state.mindmap = self.mindmap
        return self.mindmap
    
    def display_transcript(self):
        """Display the generated transcript."""
        st.text_area("Transcript", st.session_state.transcript, height=400)

    def display_summary(self):
        """Display the generated summary."""
        if st.session_state.summary:
            st.markdown("## Summary:")
            st.write(st.session_state.summary)

    def display_time_stamps(self):
        """Display the generated timestamps."""
        if st.session_state.time_stamps:
            st.markdown("## Timestamps:")
            st.markdown(st.session_state.time_stamps)
    
    def display_wordcloud(self, figsize=(10, 5)):
        """Display the generated word cloud."""
        if st.session_state.wordcloud:
            fig, ax = plt.subplots(figsize=figsize)
            ax.imshow(st.session_state.wordcloud, interpolation='bilinear')
            ax.axis("off")
            st.pyplot(fig)
            
    def display_mindmap(self):
        """Display the generated mindmap."""
        if st.session_state.mindmap:
            # 创建 NetworkX 图
            G = nx.DiGraph()

            # 解析从 OpenAI 返回的 mindmap 数据
            edges = [edge.strip() for edge in st.session_state.mindmap.split(",")]
            for edge in edges:
                nodes = [node.strip() for node in edge.split("-")]
                if len(nodes) > 1:  # 确保至少有两个节点
                    for i in range(len(nodes) - 1):
                        G.add_edge(nodes[i], nodes[i + 1])
                else:
                    st.warning(f"跳过无效输入: {edge}")

            # 创建 Pyvis Network 对象
            net = Network(height="750px", width="100%", directed=True)

            # 将 NetworkX 图添加到 Pyvis 网络中
            for node in G.nodes():
                net.add_node(node, color='purple')

            for edge in G.edges():
                net.add_edge(edge[0], edge[1], color='purple')

            # 自定义节点和边的外观
            net.repulsion(node_distance=100, central_gravity=0.33,
                          spring_length=30, spring_strength=0.10,
                          damping=0.95)

            # 生成 HTML 文件并显示
            net.write_html("mindmap.html")
            HtmlFile = open("mindmap.html", 'r', encoding='utf-8')
            source_code = HtmlFile.read()
            components.html(source_code, height=750, width=1000)