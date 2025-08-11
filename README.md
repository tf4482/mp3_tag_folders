# 🎵 MP3 Tag Folders

A Python tool for automatically updating MP3 album tags based on folder names. The tool works recursively through subdirectories and provides colorful output with emojis for better user experience.

## ✨ Features

- 🎵 **Automatic album tag updates** based on folder names
- ⚡ **Smart tag comparison** - skips files where tags are already correct
- 🔄 **Recursive processing** of subdirectories
- 🎨 **Colorful console output** with meaningful emojis
- 🧹 **Smart name cleaning** (removes punctuation, normalizes whitespace)
- 📁 **Multiple directories** processing at once
- 🛡️ **Robust error handling** with detailed messages
- 🏷️ **ID3 tag support** with automatic tag creation

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- Poetry (recommended) or pip

### With Poetry (recommended)

```bash
# Clone repository
git clone <repository-url>
cd mp3_tag_folders

# Install dependencies
poetry install

# Run the tool
poetry run mp3_tag_folders /path/to/music/folder
```

### With pip

```bash
# Install dependencies
pip install mutagen colorama

# Run script directly
python mp3_tag_folders.py /path/to/music/folder
```

## 📖 Usage

### Basic Syntax

```bash
mp3_tag_folders <directory1> [<directory2> ...]
```

### Examples

```bash
# Process single directory
mp3_tag_folders /home/user/Music/Podcasts

# Process multiple directories at once
mp3_tag_folders /home/user/Music/Album1 /home/user/Music/Album2

# Process current directory
mp3_tag_folders .
```

### Output Example

```
🔄 Processing directory: /home/user/Music/My Album
🎵 Updated album tag for song1.mp3 → 'My Album'
⏭️ Skipped song2.mp3 (album tag already correct: 'My Album')
🎵 Updated album tag for song3.mp3 → 'My Album'
✅ Album tagging for /home/user/Music/My Album/Bonus Tracks done.
🎵✨ All MP3 files in '/home/user/Music/My Album' and its subdirectories have been updated.
```

## 🎯 How It Works

1. **Folder Analysis**: The tool reads the folder name and cleans it by removing punctuation and normalizing whitespace
2. **MP3 Discovery**: Finds all `.mp3` files in the current directory (non-recursive for files)
3. **Tag Comparison**: Checks if the current album tag already matches the target value
4. **Smart Update**: Only writes tags when changes are actually needed, improving performance
5. **Recursive Processing**: Processes all subdirectories recursively
6. **Progress Reporting**: Provides real-time feedback with colorful emoji indicators

## 📊 Status Indicators

The tool uses various emojis to indicate different states:

- 🔄 **Processing**: Currently working on a directory
- 🎵 **Updated**: Successfully updated an MP3 file's album tag
- ⏭️ **Skipped**: File skipped because album tag is already correct
- ✅ **Complete**: Finished processing a subdirectory
- ❌ **Error**: Failed to update a file or access a directory
- 🚫 **Permission**: Permission denied errors
- 📁❌ **Not Found**: Directory not found
- ℹ️ **Info**: Usage information
- 🎵✨ **Final**: All processing completed successfully

## 🛠️ Dependencies

- **[mutagen](https://mutagen.readthedocs.io/)**: For MP3 metadata manipulation
- **[colorama](https://pypi.org/project/colorama/)**: For cross-platform colored terminal output

## 📝 Example Directory Structure

```
Music/
├── The Beatles - Abbey Road/
│   ├── 01 - Come Together.mp3
│   ├── 02 - Something.mp3
│   └── Bonus Tracks/
│       └── 03 - Her Majesty.mp3
└── Pink Floyd - Dark Side of the Moon/
    ├── 01 - Speak to Me.mp3
    └── 02 - Breathe.mp3
```

After running `mp3_tag_folders Music/`:
- All files in "The Beatles - Abbey Road/" get album tag: "The Beatles Abbey Road"
- All files in "Bonus Tracks/" get album tag: "Bonus Tracks"
- All files in "Pink Floyd - Dark Side of the Moon/" get album tag: "Pink Floyd Dark Side of the Moon"

## 🔧 Command Line Options

```bash
mp3_tag_folders --help          # Show help message
mp3_tag_folders --version       # Show version information
mp3_tag_folders <directories>   # Process specified directories
```

## 📄 License

This project is licensed under the terms specified in the LICENSE file.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## 📧 Support

If you encounter any issues or have questions, please open an issue on the project repository.
