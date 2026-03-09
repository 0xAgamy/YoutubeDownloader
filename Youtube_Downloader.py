import argparse
import sys
import yt_dlp as youtube_dl
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm



logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

file_handler = logging.FileHandler('youtube_downloader.log')
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


class DownloadProgress:
    """Handles per-video tqdm progress bar."""

    def __init__(self, overall_bar=None):
        self.pbar = None
        self.overall_bar = overall_bar  # reference to the overall progress bar
        self._last_downloaded = 0

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            if self.pbar is None:
                total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                filename = d.get('filename', 'video')
                # Trim filename for display
                short_name = filename.split('/')[-1][:40]
                self.pbar = tqdm(
                    total=total if total else None,
                    unit='B',
                    unit_scale=True,
                    unit_divisor=1024,
                    desc=f"  ↳ {short_name}",
                    leave=False,
                    bar_format='{desc}: {percentage:3.0f}%|{bar:30}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]',
                    colour='cyan',
                    dynamic_ncols=True,
                )
                self._last_downloaded = 0

            if self.pbar:
                downloaded = d.get('downloaded_bytes', 0)
                self.pbar.update(downloaded - self._last_downloaded)
                self._last_downloaded = downloaded

        elif d['status'] == 'finished':
            if self.pbar:
                self.pbar.close()
                self.pbar = None
            self._last_downloaded = 0




def get_ydl_opts(output_path, fmt, subtitles, subtitle_langs, progress_hook, is_playlist=False):
    template = f'{output_path}/%(playlist)s/%(title)s.%(ext)s' if is_playlist else f'{output_path}/%(title)s.%(ext)s'
    opts = {
        'outtmpl': template,
        'format': fmt,
        'merge_output_format': 'mp4',
        'progress_hooks': [progress_hook],
        'quiet': True,
        'no_warnings': True,
        'noprogress': True,
    }
    if subtitles:
        opts['writesubtitles'] = True
        if subtitle_langs:
            opts['subtitleslangs'] = subtitle_langs
        else:
            opts['allsubtitles'] = True
    return opts


def download_with_retries(func, *args, retries=3, delay=5, **kwargs):
    attempt = 0
    while attempt < retries:
        try:
            func(*args, **kwargs)
            return True
        except Exception as e:
            attempt += 1
            if attempt < retries:
                logger.warning(f"Retry {attempt}/{retries} - {str(e)}")
                time.sleep(delay)
            else:
                logger.error(f"Failed after {retries} attempts: {str(e)}")
                return False


def download_video(video_url, output_path='.', fmt='bestvideo+bestaudio/best',
                   subtitles=False, subtitle_langs=None, overall_bar=None):
    progress = DownloadProgress(overall_bar=overall_bar)
    ydl_opts = get_ydl_opts(output_path, fmt, subtitles, subtitle_langs, progress.progress_hook)

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        logger.info(f"Downloaded: {video_url}")
    except Exception as e:
        logger.error(f"Error downloading {video_url}: {str(e)}")
        raise


def download_playlist(playlist_url, output_path='.', fmt='bestvideo+bestaudio/best',
                      subtitles=False, subtitle_langs=None):
    
    extract_opts = {'quiet': True, 'no_warnings': True, 'extract_flat': True}
    with youtube_dl.YoutubeDL(extract_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)
        total = len(info.get('entries', [])) if info else 0
        playlist_title = info.get('title', 'Playlist') if info else 'Playlist'

    overall_bar = tqdm(
        total=total,
        desc=f"📋 {playlist_title[:50]}",
        unit='video',
        bar_format='{desc}: {percentage:3.0f}%|{bar:40}| {n}/{total} videos [{elapsed}<{remaining}]',
        colour='green',
        dynamic_ncols=True,
    )

    completed = [0]

    def per_video_hook(d):
        if d['status'] == 'finished':
            completed[0] += 1
            overall_bar.update(1)
            overall_bar.set_postfix_str(f"✓ {completed[0]}/{total} done")

    progress = DownloadProgress()

    def combined_hook(d):
        progress.progress_hook(d)
        per_video_hook(d)

    ydl_opts = get_ydl_opts(output_path, fmt, subtitles, subtitle_langs, combined_hook, is_playlist=True)

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([playlist_url])
        logger.info(f"Downloaded playlist: {playlist_url}")
    except Exception as e:
        logger.error(f"Error downloading playlist: {str(e)}")
        raise
    finally:
        overall_bar.close()


def download_multiple_videos(video_urls, output_path='.', fmt='bestvideo+bestaudio/best',
                              subtitles=False, subtitle_langs=None):
    total = len(video_urls)

    overall_bar = tqdm(
        total=total,
        desc="🎬 Overall Progress",
        unit='video',
        bar_format='{desc}: {percentage:3.0f}%|{bar:40}| {n}/{total} videos [{elapsed}<{remaining}]',
        colour='green',
        dynamic_ncols=True,
    )

    def run_download(url):
        success = download_with_retries(
            download_video, url, output_path, fmt, subtitles, subtitle_langs
        )
        overall_bar.update(1)
        overall_bar.set_postfix_str(f"Last: {url.split('=')[-1][:20]}")
        return success

   
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(run_download, url) for url in video_urls]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                logger.error(f"Failed: {str(e)}")

    overall_bar.close()


def main():
    parser = argparse.ArgumentParser(description="YouTube Video Downloader")
    parser.add_argument("--video", help="Download a single video")
    parser.add_argument("--playlist", help="Download a playlist")
    parser.add_argument("--multiple", nargs='+', help="Download multiple videos")
    parser.add_argument("--output", default=".", help="Output directory (default: current directory)")
    parser.add_argument("--format", default="bestvideo+bestaudio/best", help="Video format")
    parser.add_argument("--subtitles", action="store_true", help="Download subtitles")
    parser.add_argument("--subtitle-langs", nargs='+', help="Subtitle languages (e.g. en fr)")

    args = parser.parse_args()

    try:
        if args.video:
            progress = DownloadProgress()
            ydl_opts = get_ydl_opts(
                args.output, args.format, args.subtitles,
                args.subtitle_langs, progress.progress_hook
            )
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([args.video])

        elif args.playlist:
            download_playlist(
                args.playlist, args.output, args.format,
                args.subtitles, args.subtitle_langs
            )

        elif args.multiple:
            download_multiple_videos(
                args.multiple, args.output, args.format,
                args.subtitles, args.subtitle_langs
            )

        else:
            parser.print_help()
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n⚠️  Download interrupted by user.")
        sys.exit(0)


if __name__ == "__main__":
    main()