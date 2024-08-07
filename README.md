# YouTube Video Downloader
## Overview 
This script allows you to download videos and playlists from YouTube using the `yt_dlp` library. It supports downloading single videos, entire playlists, and multiple videos concurrently. The script also supports downloading subtitles in specified languages.
## Features 
- **Download Single Video:** Download a single video from YouTube.
- **Download Playlist:** Download an entire playlist from YouTube.
- **Download Multiple Videos:** Download multiple videos concurrently. 
- **Custom Output Directory:** Specify the directory where the downloaded files will be saved. - **Format Selection:** Choose the format of the downloaded video. 
- **Subtitles Support:** Download subtitles in specified languages

## Requirements 
- Python 3.9+
- `yt_dlp` library 
- `tqdm` library 
- `ffmpeg` software 

## Installation To install the required libraries, run: 
```bash 

pip install yt-dlp tqdm
```

### Installing ffmpeg

#### Windows

Download the ffmpeg zip file from the [official site](https://ffmpeg.org/download.html), extract it, and add the `bin` folder to your system's PATH.

#### macOS

You can install ffmpeg using Homebrew:

`brew install ffmpeg`

#### Linux

You can install ffmpeg using your distribution's package manager. For example, on Ubuntu:
```bash
sudo apt update sudo apt install ffmpeg

```

## Usage

The script can be run from the command line. Below are the available options:

### Command Line Arguments

- `--video`: URL of the video to download.
- `--playlist`: URL of the playlist to download.
- `--multiple`: URLs of multiple videos to download (space-separated).
- `--output`: Output directory (default: current directory).
- `--format`: Video format (default: `bestvideo+bestaudio/best`).
- `--subtitles`: Download subtitles (flag).
- `--subtitle-langs`: Specify subtitle languages (e.g., `en fr de`).

### Examples

#### Download a Single Video

```bash
python Youtube_Downloader.py --video <video_url> --output <output_directory> --format <format> --subtitles --subtitle-langs en`
```
#### Download a Playlist

``` bash
python Youtube_Downloader.py --playlist <playlist_url> --output <output_directory> --format <format> --subtitles --subtitle-langs en`
```

#### Download Multiple Videos

``` bash
python Youtube_Downloader.py --multiple <video_url1> <video_url2> <video_url3> --output <output_directory> --format <format> --subtitles --subtitle-langs en`
```

### Options Description

- **--video**: Downloads a single video from the provided URL.
- **--playlist**: Downloads an entire playlist from the provided URL.
- **--multiple**: Downloads multiple videos concurrently from the provided URLs.
- **--output**: Specifies the directory where the downloaded files will be saved. Default is the current directory.
- **--format**: Specifies the format of the downloaded video. Default is `bestvideo+bestaudio/best`.
- **--subtitles**: Downloads subtitles if available.
- **--subtitle-langs**: Specifies the languages of subtitles to download (e.g., `en fr de`). If not specified, all available subtitles are downloaded.

## Logging

The script uses logging to provide information about the download process. Logs include timestamps and log levels (INFO, ERROR).

## Progress Bar

The script uses `tqdm` to display a progress bar for each download, showing the progress of the download in bytes.

## Error Handling

The script includes basic error handling to log errors and provide feedback if something goes wrong during the download process.

## Contribution

Feel free to fork this repository and contribute by submitting pull requests. Please ensure your code adheres to the existing style and structure.


## Contact

For any questions or suggestions, please contact [mohamedelagamy516@gmail.com].
