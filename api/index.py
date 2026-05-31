#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify, request
from datetime import datetime
from config import Config
from youtube_scraper import YouTubeScraper
from content_processor import ContentProcessor

app = Flask(__name__)
scraper = YouTubeScraper()
processor = ContentProcessor()


@app.route('/')
def index():
    return jsonify({
        'status': 'ok',
        'message': 'Greyhound Lines API is running'
    })


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


# Vercel 需要这个
handler = app
