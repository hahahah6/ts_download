# TS Downloader

A Python script to download .ts files from m3u8 playlists, handle AES encryption, and convert them to MP4 format using ffmpeg.

## Features

- Download .ts segments from m3u8 playlists
- Handle AES encryption automatically
- Concurrent downloading for faster processing
- Merge segments into a single .ts file
- Convert to MP4 format using ffmpeg
- Cross-platform support (Windows, Linux, macOS)
- Progress tracking with tqdm
- Automatic retry mechanism for failed downloads

## Installation

1. Clone or download this repository
2. Install required Python packages:

```bash
pip install -r requirements.txt
```

3. Download ffmpeg binary for your platform and place it in the appropriate directory:
   - Windows: `ffmpeg/windows/ffmpeg.exe`
   - Linux: `ffmpeg/linux/ffmpeg`
   - macOS: `ffmpeg/mac/ffmpeg`

## Usage

1. Open [run.py](run.py) and set your m3u8 URL:

```python
m3u8_url = "https://example.com/playlist.m3u8"  # Replace with your m3u8 URL
```

2. Configure settings (optional):

```python
output_dir = "ts_concurrent"    # Output directory for .ts files
merged_file = "merged.ts"       # Merged .ts file name
final_output = "output.mp4"     # Final MP4 output name
max_workers = 100               # Number of concurrent download threads
max_retries = 10                # Retry attempts for failed downloads
timeout_sec = 10                # Request timeout in seconds
```

3. Run the script:

```bash
python run.py
```

## How It Works

1. **Load Playlist**: Downloads and parses the m3u8 playlist
2. **Check Encryption**: Detects AES encryption and downloads the key if present
3. **Download Segments**: Downloads all .ts segments concurrently with retry mechanism
4. **Decrypt**: Decrypts segments if encryption is detected
5. **Merge**: Combines all segments into a single .ts file
6. **Convert**: Uses ffmpeg to convert the merged file to MP4

## Dependencies

- `m3u8`: For parsing m3u8 playlists
- `requests`: For HTTP requests
- `pycryptodome`: For AES decryption
- `tqdm`: For progress bars
- `concurrent.futures`: For concurrent downloading

See [requirements.txt](requirements.txt) for complete dependency list.

## Platform Support

The script automatically detects your platform and uses the appropriate ffmpeg binary:

- **Windows**: Uses `ffmpeg/windows/ffmpeg.exe`
- **Linux**: Uses `ffmpeg/linux/ffmpeg`
- **macOS**: Uses `ffmpeg/mac/ffmpeg`

## Output Files

The script generates the following files (automatically cleaned up on each run):

- `ts_concurrent/`: Directory containing individual .ts segments
- `merged.ts`: Combined .ts file
- `output.mp4`: Final MP4 video file

These files are ignored by git (see [.gitignore](.gitignore)).

## Configuration

You can modify the following settings at the top of [run.py](run.py):

| Setting | Default | Description |
|---------|---------|-------------|
| `max_workers` | 100 | Number of concurrent download threads |
| `max_retries` | 10 | Maximum retry attempts for failed downloads |
| `timeout_sec` | 10 | HTTP request timeout in seconds |
| `output_dir` | "ts_concurrent" | Directory for downloaded segments |
| `merged_file` | "merged.ts" | Name of the merged .ts file |
| `final_output` | "output.mp4" | Name of the final MP4 file |

## Error Handling

- Automatic retry mechanism for failed downloads
- Progress tracking for download status
- Platform detection for ffmpeg execution
- Missing ffmpeg binary detection

## License

Copyright (c) 2025 by hahahah6, All Rights Reserved.

## Requirements

- Python 3.12+
- ffmpeg binary for your platform
- Internet connection for downloading segments

## Troubleshooting

1. **ffmpeg not found**: Make sure ffmpeg is placed in the correct directory for your platform
2. **Download failures**: Check your internet connection and the m3u8 URL
3. **Encryption errors**: Ensure the encryption key is accessible from the m3u8 URL
4. **Permission errors**: Make sure you have write permissions in the current directory