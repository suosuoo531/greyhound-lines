import random
import requests
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from config import Config


class YouTubeScraper:
    def __init__(self):
        self.used_locations = set()
        self.api_key = None

    def get_random_location(self):
        locations = Config.US_STATES + Config.US_CITIES
        available = [loc for loc in locations if loc not in self.used_locations]
        
        if not available:
            self.used_locations.clear()
            available = locations
        
        location = random.choice(available)
        self.used_locations.add(location)
        return location

    def search_video(self, location):
        search_queries = [
            f"{location} local guide",
            f"{location} hidden gems",
            f"{location} walking tour",
            f"{location} neighborhood guide",
            f"{location} city walk",
            f"{location} what locals do"
        ]
        
        avoid_keywords = ['travel vlog', 'vlog', 'day in the life', 'my trip', 'what i did', 'my journey']
        
        try:
            for query in search_queries:
                video_ids = self._search_video_ids(query, avoid_keywords)
                if video_ids:
                    return video_ids[0]
            
            return None
        except Exception as e:
            print(f"Error searching video for {location}: {e}")
            return None

    def _search_video_ids(self, query, avoid_keywords):
        try:
            from pytube import Search
            s = Search(query)
            videos = s.results[:10]
            
            filtered_videos = []
            for video in videos:
                title = video.title.lower()
                has_avoid = any(keyword in title for keyword in avoid_keywords)
                
                if not has_avoid and video.length < 3600 and video.length > 180:
                    filtered_videos.append(video.video_id)
            
            return filtered_videos
        except Exception as e:
            print(f"Error in video search: {e}")
            return []

    def get_transcript(self, video_id):
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            transcript = None
            if transcript_list.find_transcript(['en']):
                transcript = transcript_list.find_transcript(['en'])
            else:
                transcript = transcript_list.find_generated_transcript(['en'])
            
            if transcript:
                formatter = TextFormatter()
                return formatter.format_transcript(transcript.fetch())
            return None
        except Exception as e:
            print(f"Error getting transcript: {e}")
            return None

    def get_video_info(self, video_id):
        try:
            from pytube import YouTube
            yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
            return {
                'title': yt.title,
                'url': yt.watch_url,
                'thumbnail_url': yt.thumbnail_url,
                'author': yt.author,
                'length': yt.length
            }
        except Exception as e:
            print(f"Error getting video info: {e}")
            return None
