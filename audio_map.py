import os
import sys
import warnings
import torch
from pathlib import Path

# Suppress warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="whisper")
warnings.filterwarnings("ignore", category=UserWarning, module="whisper")

project_dir = os.path.dirname(os.path.abspath(__file__))
if project_dir not in sys.path:
    sys.path.append(project_dir)

try:
    from src.transcriber import AudioTranscriber
    import shutil
except ImportError as e:
    print(f"Import error: {e}")
    raise

class AudioMap:
    def __init__(self):
        self.base_dir = Path("audio_map")
        self.audio_dir = self.base_dir / "audio"
        self.transcripts_dir = self.base_dir / "transcripts"
        
        self.audio_dir.mkdir(parents=True, exist_ok=True)
        self.transcripts_dir.mkdir(parents=True, exist_ok=True)
        
        self.transcriber = AudioTranscriber()

    def transcribe_existing(self, index):
        audio_files = list(self.audio_dir.glob("*"))
        if 1 <= index <= len(audio_files):
            selected_file = audio_files[index - 1]
            print(f"\nTranscribing: {selected_file.name}")
            
            print("\nChoose transcription mode:")
            print("1. Auto (default Whisper settings)")
            print("2. Manual (customize settings)")
            mode_choice = input("Enter choice (1-2): ")
            
            kwargs = {}
            if mode_choice == "2":
                print("\nManual Configuration:")
                lines = input("How many lines per segment? (default: 2): ")
                if lines.strip():
                    kwargs['lines_per_segment'] = int(lines)
                
                duration = input("Target duration in seconds? (default: 12.0): ")
                if duration.strip():
                    kwargs['target_duration'] = float(duration)
                
                chars = input("Character limit per segment? (default: 175): ")
                if chars.strip():
                    kwargs['char_limit'] = int(chars)
                
                print("\nChoose segmentation mode:")
                print("1. Auto (Whisper default)")
                print("2. Duration-based")
                print("3. Lines-based")
                print("4. Character-based")
                seg_mode = input("Enter choice (1-4): ")
                
                mode_map = {
                    "1": "auto",
                    "2": "duration",
                    "3": "lines",
                    "4": "chars"
                }
                kwargs['mode'] = mode_map.get(seg_mode, "auto")
            
            self.transcriber.transcribe(
                str(selected_file), 
                str(self.transcripts_dir),
                **kwargs
            )
            print("Transcription complete!")
        else:
            print("Invalid selection!")

    def add_audio(self, audio_path):
        try:
            audio_path = Path(audio_path)
            if not audio_path.exists():
                print(f"File not found: {audio_path}")
                return
            
            # Copy audio file to audio directory
            shutil.copy2(audio_path, self.audio_dir)
            new_path = self.audio_dir / audio_path.name
            print(f"Added and transcribed: {audio_path.name}")
            
            # Transcribe the file
            self.transcriber.transcribe(str(new_path), str(self.transcripts_dir))
            
        except Exception as e:
            print(f"Error processing {audio_path}: {e}")

    def list_files(self):
        print("\nAvailable audio files:")
        audio_files = list(self.audio_dir.glob("*"))
        for i, file in enumerate(audio_files, 1):
            print(f"{i}. {file.name}")
        return audio_files

def main():
    audio_map = AudioMap()
    
    while True:
        print("\n=== MENU ===")
        print("1. Add new audio file")
        print("2. List files")
        print("3. Select and transcribe existing file")
        print("4. Exit")
        
        choice = input("\nChoose an option (1-4): ")
        
        if choice == "1":
            audio_path = input("Enter path to audio file: ")
            audio_map.add_audio(audio_path)
        elif choice == "2":
            audio_map.list_files()
        elif choice == "3":
            files = audio_map.list_files()
            if files:
                try:
                    index = int(input("\nEnter the number of the file to transcribe: "))
                    audio_map.transcribe_existing(index)
                except ValueError:
                    print("Please enter a valid number!")
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Please choose 1-4")

if __name__ == "__main__":
    main() 