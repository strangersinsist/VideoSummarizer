from youtube_transcript_api import YouTubeTranscriptApi
# import strip_markdown

class Method:
    @staticmethod
    def Id(link):
        """Extracts video ID from YouTube link."""
        if "watch?v=" in link:
            return link.split("watch?v=")[1]
        elif "youtu.be/" in link:
            return link.split("youtu.be/")[1]
        else:
            return None

    @staticmethod
    def transcript(link):
        """Gets the transcript of a YouTube video."""
        video_id = Method.Id(link)

        if not video_id:
            return "Invalid YouTube link."

        try:
            transcript_dict = YouTubeTranscriptApi.get_transcript(video_id)
            final_transcript = " ".join(i["text"] for i in transcript_dict)
            return final_transcript
        except Exception as e:
            return str(e)

    @staticmethod
    def transcript_time(link):
        """Gets the transcript with timestamps of a YouTube video."""
        video_id = Method.Id(link)

        if not video_id:
            return "Invalid YouTube link."

        try:
            transcript_dict = YouTubeTranscriptApi.get_transcript(video_id)
            transcript_with_time = "\n".join(
                f"{i['start']} - {i['text']}" for i in transcript_dict
            )
            return transcript_with_time
        except Exception as e:
            return str(e)
        
    # @staticmethod
    # def format(gentext):
    #     cp_text = strip_markdown.strip_markdown(gentext)
    #     return cp_text