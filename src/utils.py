from pathlib import Path
from typing import List

def get_supported_extensions() -> List[str]:
    """Return list of supported audio file extensions."""
    return ['.mp3', '.wav', '.m4a', '.ogg', '.flac']

def validate_audio_file(file_path: str) -> bool:
    """
    Validate if the file exists and has a supported extension.
    
    Args:
        file_path: Path to the audio file
        
    Returns:
        bool: True if file is valid, False otherwise
    """
    path = Path(file_path)
    return path.exists() and path.suffix.lower() in get_supported_extensions()

