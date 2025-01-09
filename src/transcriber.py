import whisper
from pathlib import Path
import datetime

class AudioTranscriber:
    def __init__(self, model_size: str = "base"):
        self.model = whisper.load_model(model_size)
    
    def combine_segments(self, segments, mode="auto", lines_per_segment=2, target_duration=12.0, char_limit=175):
        """Combine segments with configurable modes:
        - "auto": Original Whisper segmentation
        - "duration": Combine by target duration (~12 seconds)
        - "lines": Split into specific number of lines
        - "chars": Combine by character limit
        """
        if mode == "auto":
            # Return original Whisper segments with minimal formatting
            return [{
                'text': segment['text'].strip(),
                'start': segment['start'],
                'end': segment.get('end', 0)
            } for segment in segments]
            
        elif mode == "duration":
            return self._combine_by_duration(segments, target_duration)
            
        elif mode == "lines":
            return self._combine_by_lines(segments, lines_per_segment)
            
        elif mode == "chars":
            return self._combine_by_chars(segments, char_limit)
            
        else:
            raise ValueError(f"Unknown mode: {mode}")

    def _combine_by_duration(self, segments, target_duration):
        """Combine segments into chunks of target duration"""
        combined = []
        current_lines = []
        current_start = None
        current_duration = 0
        
        for i, segment in enumerate(segments):
            if current_start is None:
                current_start = segment['start']
            
            duration = segment.get('end', 0) - segment['start']
            
            if (current_duration + duration > target_duration and current_lines) or i == len(segments) - 1:
                if i == len(segments) - 1:
                    current_lines.append(segment['text'].strip())
                
                text = ' '.join(current_lines)
                combined.append({
                    'text': text,
                    'start': current_start,
                    'end': segment['start']
                })
                
                if i != len(segments) - 1:
                    current_lines = [segment['text'].strip()]
                    current_start = segment['start']
                    current_duration = duration
            else:
                current_lines.append(segment['text'].strip())
                current_duration += duration
        
        return combined

    def _combine_by_lines(self, segments, lines_per_segment):
        """Combine segments into specific number of lines"""
        combined = []
        current_lines = []
        current_start = None
        
        for i, segment in enumerate(segments):
            if current_start is None:
                current_start = segment['start']
            
            current_lines.append(segment['text'].strip())
            
            if len(current_lines) >= lines_per_segment or i == len(segments) - 1:
                text = ' \\\n        '.join(current_lines)
                combined.append({
                    'text': text,
                    'start': current_start,
                    'end': segment.get('end', 0)
                })
                current_lines = []
                current_start = None
        
        return combined

    def _combine_by_chars(self, segments, char_limit):
        """Combine segments by character limit"""
        combined = []
        current_text = []
        current_start = None
        current_chars = 0
        
        for segment in segments:
            text = segment['text'].strip()
            if current_start is None:
                current_start = segment['start']
            
            if current_chars + len(text) > char_limit and current_chars > 0:
                combined.append({
                    'text': ' '.join(current_text),
                    'start': current_start,
                    'end': segment['start']
                })
                current_text = [text]
                current_start = segment['start']
                current_chars = len(text)
            else:
                current_text.append(text)
                current_chars += len(text)
        
        if current_text:
            combined.append({
                'text': ' '.join(current_text),
                'start': current_start,
                'end': segments[-1].get('end', 0)
            })
        
        return combined

    def transcribe(self, audio_path, output_dir=None, mode="auto", **kwargs):
        # Transcribe with word-level timestamps
        result = self.model.transcribe(audio_path, word_timestamps=True)
        
        # Combine segments according to specified mode
        segments = self.combine_segments(result['segments'], mode=mode, **kwargs)
        
        # Format output path
        audio_path = Path(audio_path)
        if output_dir:
            output_path = Path(output_dir) / audio_path.with_suffix('.swift').name
        else:
            output_path = audio_path.with_suffix('.swift')
            
        # Write Swift format
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("private let segments = [\n")
            
            for segment in segments:
                start_time = f"{segment['start']:.1f}"
                text = segment['text'].replace('"', '\\"')
                
                f.write(f'    IntroTextSegment(\n')
                f.write(f'        text: """\n        {text}\n        """,\n')
                f.write(f'        timestamp: {start_time}\n')
                f.write('    ),\n')
            
            f.write("]\n")
        
        return output_path
