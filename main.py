from src.transcriber import AudioTranscriber
from src.utils import validate_audio_file
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <audio_file_path> [output_directory]")
        return
    
    audio_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not validate_audio_file(audio_path):
        print("Error: Invalid audio file or unsupported format")
        return
    
    try:
        transcriber = AudioTranscriber()
        output_file = transcriber.transcribe(audio_path, output_dir)
        print(f"Transcription completed! Check the output file: {output_file}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
