import re
from deep_translator import GoogleTranslator


class ContentProcessor:
    def __init__(self):
        self.translator = GoogleTranslator(source='auto', target='zh-CN')

    def summarize_transcript(self, transcript, max_words=500):
        if not transcript:
            return ""
        
        sentences = re.split(r'[.!?]+', transcript)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        summary = []
        word_count = 0
        
        for sentence in sentences:
            words = sentence.split()
            if word_count + len(words) <= max_words:
                summary.append(sentence)
                word_count += len(words)
            else:
                break
        
        return '. '.join(summary) + '.'

    def translate_text(self, text):
        if not text:
            return ""
        
        try:
            translated = self.translator.translate(text)
            return translated
        except Exception as e:
            print(f"Error translating text: {e}")
            return ""

    def format_bilingual_content(self, location, video_info, english_summary, chinese_summary):
        content = []
        
        content.append(f"# {location}")
        content.append("")
        
        content.append("## 视频信息 / Video Info")
        content.append(f"- 标题 / Title: {video_info.get('title', 'N/A')}")
        content.append(f"- 链接 / URL: {video_info.get('url', 'N/A')}")
        content.append(f"- 作者 / Author: {video_info.get('author', 'N/A')}")
        content.append(f"- 时长 / Length: {video_info.get('length', 0)} 秒 / seconds")
        content.append("")
        
        content.append("## 英文介绍 / English Introduction")
        content.append(english_summary)
        content.append("")
        
        content.append("## 中文介绍 / Chinese Introduction")
        content.append(chinese_summary)
        content.append("")
        
        return '\n'.join(content)
