#!/usr/bin/env python3
import os
import threading
from flask import Flask, jsonify, request
from datetime import datetime
from config import Config
from scheduler import SubscriptionScheduler
from youtube_scraper import YouTubeScraper
from content_processor import ContentProcessor

app = Flask(__name__, static_folder='static', static_url_path='')
scheduler = SubscriptionScheduler()
scraper = YouTubeScraper()
processor = ContentProcessor()
content_list = []


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/api/generate', methods=['POST'])
def generate_content():
    try:
        data = request.get_json()
        location = data.get('location')
        
        if not location:
            return jsonify({'status': 'error', 'message': 'Location is required'}), 400
        
        print(f"Generating content for: {location}")
        
        video_id = scraper.search_video(location)
        if not video_id:
            return jsonify({'status': 'error', 'message': 'No video found'}), 404
        
        print(f"Found video: {video_id}")
        
        transcript = scraper.get_transcript(video_id)
        video_info = scraper.get_video_info(video_id)
        
        if not video_info:
            return jsonify({'status': 'error', 'message': 'Failed to get video info'}), 500
        
        summary = processor.summarize_transcript(transcript) if transcript else None
        translation = processor.translate_text(summary) if summary else None
        
        result = {
            'status': 'success',
            'location': location,
            'video': {
                'id': video_id,
                'title': video_info.get('title'),
                'url': video_info.get('url'),
                'author': video_info.get('author'),
                'length': video_info.get('length')
            },
            'content': {
                'english': summary,
                'chinese': translation
            }
        }
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Error generating content: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/trigger')
def trigger():
    try:
        scheduler.run_once()
        return jsonify({'status': 'success', 'message': 'Content generation triggered'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/content')
def get_content():
    output_files = []
    if os.path.exists(Config.OUTPUT_DIR):
        files = sorted(os.listdir(Config.OUTPUT_DIR), reverse=True)
        for f in files[:10]:
            if f.endswith('.md'):
                filepath = os.path.join(Config.OUTPUT_DIR, f)
                output_files.append({
                    'filename': f,
                    'created': datetime.fromtimestamp(os.path.getctime(filepath)).isoformat()
                })
    return jsonify(output_files)


def run_flask():
    app.run(host='0.0.0.0', port=8000, debug=False)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--web':
        print("Starting web server on http://localhost:8000")
        run_flask()
    elif len(sys.argv) > 1 and sys.argv[1] == '--once':
        scheduler.run_once()
    else:
        flask_thread = threading.Thread(target=run_flask)
        flask_thread.daemon = True
        flask_thread.start()
        print("Web server running on http://localhost:8000")
        scheduler.start_scheduled()
