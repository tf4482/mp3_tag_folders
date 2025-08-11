#!/usr/bin/env python3
"""
MP3 Tag Folders - Update album tags for MP3 files based on folder names
Converted from Fish script to Python using mutagen instead of eyeD3
"""

import sys
import argparse
from pathlib import Path
from typing import List
import re

from mutagen.mp3 import MP3
from mutagen.id3 import ID3NoHeaderError, TALB
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)


def colored_print(message: str, color: str = "") -> None:
    """Print colored message"""
    print(f"{color}{message}{Style.RESET_ALL}")


def clean_album_name(album_name: str) -> str:
    """
    Clean album name by removing punctuation and normalizing whitespace
    Equivalent to: echo $album | tr -d '[:punct:]' | tr '[:blank:]' ' '
    """
    # Entferne Satzzeichen
    cleaned = re.sub(r'[^\w\s]', '', album_name)
    # Normalisiere Whitespace
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned


def update_mp3_album(file_path: Path, album_tag: str) -> tuple[bool, str]:
    """
    Update album tag for MP3 file using mutagen
    Returns (success, status) where status is 'updated', 'unchanged', or 'failed'
    """
    try:
        audio = MP3(file_path)
        if audio.tags is None:
            audio.add_tags()
            # New tags, so definitely needs an update
            audio.tags.add(TALB(encoding=3, text=album_tag))
            audio.save()
            return True, 'updated'

        # Check current album tag
        current_album = None
        if 'TALB' in audio.tags:
            current_album = str(audio.tags['TALB'].text[0]) if audio.tags['TALB'].text else None

        # Compare current tag with new tag
        if current_album == album_tag:
            return True, 'unchanged'

        # Tag has changed, update needed
        audio.tags.add(TALB(encoding=3, text=album_tag))
        audio.save()
        return True, 'updated'

    except ID3NoHeaderError:
        # File has no ID3 tags, create new ones
        try:
            audio = MP3(file_path)
            audio.add_tags()
            audio.tags.add(TALB(encoding=3, text=album_tag))
            audio.save()
            return True, 'updated'
        except Exception as e:
            colored_print(f"❌ Failed to create ID3 tags for {file_path}: {e}", Fore.RED)
            return False, 'failed'
    except Exception as e:
        colored_print(f"❌ Failed to update album tag for {file_path}: {e}", Fore.RED)
        return False, 'failed'


def find_mp3_files(directory: Path) -> List[Path]:
    """Find all MP3 files in directory (non-recursive)"""
    mp3_files = []

    try:
        for file_path in directory.iterdir():
            if file_path.is_file() and file_path.suffix.lower() == '.mp3':
                mp3_files.append(file_path)
    except PermissionError:
        colored_print(f"🚫 Permission denied accessing directory: {directory}", Fore.RED)

    return mp3_files


def update_album_tags(folder: Path) -> None:
    """
    Update album tags for all MP3 files in folder and recursively process subdirectories
    """
    if not folder.exists() or not folder.is_dir():
        colored_print(f"📁❌ Directory not found: {folder}", Fore.RED)
        return

    # Get album name from folder name
    album_name = folder.name
    album_tag = clean_album_name(album_name)

    # Process MP3 files in current directory
    mp3_files = find_mp3_files(folder)

    for mp3_file in mp3_files:
        success, status = update_mp3_album(mp3_file, album_tag)
        if success:
            if status == 'updated':
                colored_print(f"🎵 Updated album tag for {mp3_file.name} → '{album_tag}'", Fore.CYAN)
            elif status == 'unchanged':
                colored_print(f"⏭️ Skipped {mp3_file.name} (album tag already correct: '{album_tag}')", Fore.YELLOW)
        else:
            colored_print(f"❌ Failed to update album tag for {mp3_file}", Fore.RED)

    # Process subdirectories recursively
    try:
        subdirectories = [d for d in folder.iterdir() if d.is_dir()]
        for subfolder in subdirectories:
            update_album_tags(subfolder)
            colored_print(f"✅ Album tagging for {folder}/{subfolder.name} done.", Fore.GREEN)
    except PermissionError:
        colored_print(f"🚫 Permission denied accessing subdirectories in: {folder}", Fore.RED)


def main():
    """Main function - command line interface"""
    parser = argparse.ArgumentParser(
        description="Update album tags for MP3 files based on folder names",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s /path/to/music/folder
  %(prog)s folder1 folder2 folder3
  %(prog)s .
        """
    )

    parser.add_argument(
        'directories',
        nargs='+',
        help='One or more directories to process'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 0.1.0'
    )

    args = parser.parse_args()

    if not args.directories:
        colored_print(f"ℹ️ Usage: {sys.argv[0]} <directory1> [<directory2> ...]", Fore.YELLOW)
        sys.exit(1)

    # Process each target directory
    for target_directory in args.directories:
        target_path = Path(target_directory).resolve()

        if not target_path.exists():
            colored_print(f"❌ Error: Directory '{target_directory}' not found.", Fore.RED)
            continue

        if not target_path.is_dir():
            colored_print(f"❌ Error: '{target_directory}' is not a directory.", Fore.RED)
            continue

        colored_print(f"🔄 Processing directory: {target_path}", Fore.YELLOW)
        update_album_tags(target_path)
        colored_print(f"🎵✨ All MP3 files in '{target_directory}' and its subdirectories have been updated.", Fore.MAGENTA)


if __name__ == "__main__":
    main()
