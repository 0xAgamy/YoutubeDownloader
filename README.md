# YouTube Video Downloader
## Overview 
This command-line tool lets you download YouTube videos and playlists using the `yt-dlp` library. It supports downloading single videos, entire playlists, and multiple videos concurrently. The script also supports downloading subtitles in specified languages.
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

| Argument | Description |
|---|---|
| `--video <url>` | Download a single video from the given URL |
| `--playlist <url>` | Download an entire playlist |
| `--multiple <url1> <url2> ...` | Download multiple videos (space-separated URLs) |
| `--output <dir>` | Output directory (default: current directory) |
| `--format <fmt>` | Video format string (default: `bestvideo+bestaudio/best`) |
| `--subtitles` | Enable subtitle download |
| `--subtitle-langs <lang...>` | Subtitle languages to download, e.g. `en fr de` |

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


## Logging

All activity is logged to youtube_downloader.log in the working directory. Log entries include timestamps and severity levels (INFO, WARNING, ERROR). Nothing is printed to the console beyond the progress bars
## Progress Bar

The downloader uses a two-level tqdm progress bar system designed to keep the terminal clean while showing all relevant download details.

- Per-video bar (cyan): shows filename, bytes downloaded, transfer speed, and ETA. Disappears cleanly after each video finishes.
- Overall bar (green): shown for playlists and batch downloads. Tracks how many videos have completed out of the total. Persists until all downloads are done.
## Error Handling

The script includes basic error handling to log errors and provide feedback if something goes wrong during the download process.

## Contribution

Feel free to fork this repository and contribute by submitting pull requests. Please ensure your code adheres to the existing style and structure.


## Contact

For any questions or suggestions, please contact [mohamedelagamy516@gmail.com].
