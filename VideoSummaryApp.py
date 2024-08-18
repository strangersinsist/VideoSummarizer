# VideoSummaryApp.py

import streamlit as st
from model import Model
from prompt import Prompt
from method import Method

class VideoSummaryApp:
    def __init__(self):
        self.video_transcript = ""
        self.summary = ""
        self.video_transcript_time = ""
        self.time_stamps = ""

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
