import argparse
import sys
import yt_dlp as youtube_dl
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from plyer import notification

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

file_handler = logging.FileHandler('youtube_downloader.log')
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

class DownloadProgress:
    def __init__(self):
        self.pbar = None

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            if self.pbar is None:
                total = d.get('total_bytes') or d.get('total_bytes_estimate')
                if total:
                    self.pbar = tqdm(total=total, unit='B', unit_scale=True, desc=d['filename'])
            if self.pbar:
                downloaded = d.get('downloaded_bytes', 0)
                self.pbar.n = downloaded
                self.pbar.last_print_n = downloaded
                self.pbar.refresh()
        elif d['status'] == 'finished' and self.pbar:
            self.pbar.n = self.pbar.total
            self.pbar.last_print_n = self.pbar.total
            self.pbar.refresh()
            self.pbar.close()
            self.pbar = None
            print(f"Finished downloading {d['filename']}")

def notify(title, message):
    notification.notify(
        title=title,
        message=message,
        app_name='YouTube Downloader',
        timeout=10,
    )

def download_with_retries(func, *args, retries=3, delay=5, **kwargs):
    attempt = 0
    while attempt < retries:
        try:
            func(*args, **kwargs)
            return
        except Exception as e:
            attempt += 1
            if attempt < retries:
                logger.warning(f"Error downloading: {str(e)}. Retrying {attempt}/{retries}...")
                time.sleep(delay)
            else:
                logger.error(f"Failed after {retries} attempts: {str(e)}")

def download_video(video_url, output_path='.', format='bestvideo+bestaudio/best', subtitles=False, subtitle_langs=None):
    progress = DownloadProgress()
    ydl_opts = {
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'format': format,
        'merge_output_format': 'mp4',
        'progress_hooks': [progress.progress_hook],
    }
    if subtitles:
        ydl_opts['writesubtitles'] = True
        if subtitle_langs:
            ydl_opts['subtitleslangs'] = subtitle_langs
        else:
            ydl_opts['allsubtitles'] = True

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        logger.info(f"Successfully downloaded: {video_url}")
        notify("Download Complete", f"Successfully downloaded: {video_url}")
    except Exception as e:
        logger.error(f"Error downloading {video_url}: {str(e)}")
        notify("Download Failed", f"Error downloading {video_url}: {str(e)}")
        raise e  # Re-raise the exception to handle retries

def download_playlist(playlist_url, output_path='.', format='bestvideo+bestaudio/best', subtitles=False, subtitle_langs=None):
    progress = DownloadProgress()
    ydl_opts = {
        'outtmpl': f'{output_path}/%(playlist)s/%(title)s.%(ext)s',
        'format': format,
        'merge_output_format': 'mp4',
        'progress_hooks': [progress.progress_hook],
    }
    if subtitles:
        ydl_opts['writesubtitles'] = True
        if subtitle_langs:
            ydl_opts['subtitleslangs'] = subtitle_langs
        else:
            ydl_opts['allsubtitles'] = True

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([playlist_url])
        logger.info(f"Successfully downloaded playlist: {playlist_url}")
        notify("Download Complete", f"Successfully downloaded playlist: {playlist_url}")
    except Exception as e:
        logger.error(f"Error downloading playlist {playlist_url}: {str(e)}")
        notify("Download Failed", f"Error downloading playlist {playlist_url}: {str(e)}")
        raise e  # Re-raise the exception to handle retries

def download_multiple_videos(video_urls, output_path='.', format='bestvideo+bestaudio/best', subtitles=False, subtitle_langs=None):
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(download_with_retries, download_video, url, output_path, format, subtitles, subtitle_langs) for url in video_urls]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                logger.error(f"Failed to download video: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="YouTube Video Downloader")
    parser.add_argument("--video", help="Download a single video")
    parser.add_argument("--playlist", help="Download a playlist")
    parser.add_argument("--multiple", nargs='+', help="Download multiple videos")
    parser.add_argument("--output", default=".", help="Output directory (default: current directory)")
    parser.add_argument("--format", default="bestvideo+bestaudio/best", help="Video format (default: best quality)")
    parser.add_argument("--subtitles", action="store_true", help="Download subtitles")
    parser.add_argument("--subtitle-langs", nargs='+', help="Specify subtitle languages (e.g., en fr de)")

    args = parser.parse_args()

    try:
        if args.video:
            download_with_retries(download_video, args.video, args.output, args.format, args.subtitles, args.subtitle_langs)
        elif args.playlist:
            download_with_retries(download_playlist, args.playlist, args.output, args.format, args.subtitles, args.subtitle_langs)
        elif args.multiple:
            download_multiple_videos(args.multiple, args.output, args.format, args.subtitles, args.subtitle_langs)
        else:
            parser.print_help()
            sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Download interrupted by user.")
        sys.exit(0)

if __name__ == "__main__":
    main()
