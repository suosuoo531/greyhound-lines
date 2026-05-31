import os
import time
import schedule
from datetime import datetime
from config import Config
from youtube_scraper import YouTubeScraper
from content_processor import ContentProcessor


class SubscriptionScheduler:
    def __init__(self):
        self.scraper = YouTubeScraper()
        self.processor = ContentProcessor()
        
        if not os.path.exists(Config.OUTPUT_DIR):
            os.makedirs(Config.OUTPUT_DIR)

    def run_once(self):
        print(f"\n{'='*60}")
        print(f"Starting content generation at {datetime.now()}")
        print('='*60)
        
        location = self.scraper.get_random_location()
        print(f"Selected location: {location}")
        
        video_id = self.scraper.search_video(location)
        if not video_id:
            print(f"No video found for {location}")
            return
        
        print(f"Found video ID: {video_id}")
        
        video_info = self.scraper.get_video_info(video_id)
        if not video_info:
            print("Could not get video info")
            return
        
        transcript = self.scraper.get_transcript(video_id)
        if not transcript:
            print("Could not get transcript")
            return
        
        print("Transcript retrieved successfully")
        
        english_summary = self.processor.summarize_transcript(transcript)
        chinese_summary = self.processor.translate_text(english_summary)
        
        bilingual_content = self.processor.format_bilingual_content(
            location, video_info, english_summary, chinese_summary
        )
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{location.replace(' ', '_')}_{timestamp}.md"
        filepath = os.path.join(Config.OUTPUT_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(bilingual_content)
        
        print(f"Content saved to: {filepath}")
        print(f"Completed at {datetime.now()}")
        print(f"{'='*60}\n")

    def start_scheduled(self):
        for day in Config.SCHEDULE_DAYS:
            getattr(schedule.every(), day).at(Config.SCHEDULE_TIME).do(self.run_once)
        
        print(f"Scheduler started. Running every {', '.join(Config.SCHEDULE_DAYS)} at {Config.SCHEDULE_TIME}")
        print("Press Ctrl+C to stop\n")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)
        except KeyboardInterrupt:
            print("\nScheduler stopped.")
