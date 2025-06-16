'''
Author: hahahah6 tensorrt@163.com
Date: 2025-06-15 21:55:42
LastEditors: hahahah6 tensorrt@163.com
LastEditTime: 2025-06-16 11:50:39
FilePath: \ts_download\run.py
Description: This script downloads .ts files from a given m3u8 playlist URL, handles AES encryption if present, merges the segments into a single .ts file, and converts it to MP4 format using ffmpeg.

Copyright (c) 2025 by hahahah6, All Rights Reserved. 
'''


import os
import m3u8
import requests
from urllib.parse import urljoin
from tqdm import tqdm
from Crypto.Cipher import AES
from concurrent.futures import ThreadPoolExecutor
import shutil
import platform

# ======= Configuration =======
m3u8_url = "" # Replace with your m3u8 URL or file path
output_dir = "ts_concurrent"
merged_file = "merged.ts"
final_output = "output.mp4"
file_path = os.path.dirname(os.path.abspath(__file__))

max_workers = 100
max_retries = 10
timeout_sec = 10
# =============================

# Global shared values
ts_urls = []
aes_key = None
iv = None
ffmpeg_path = None
def check_ffmpeg():
    if not os.path.exists(ffmpeg_path):
        raise FileNotFoundError(f"ffmpeg not found at {ffmpeg_path}. Please download it and place it in the 'ffmpeg' directory.")

import shutil  # 确保引入这个模块用于删除文件夹

def create_output_dir():
    global ts_urls, aes_key, iv

    # Clean up old output folder and files
    if os.path.exists(output_dir):
        print(f"[!] Removing old output directory: {output_dir}")
        shutil.rmtree(output_dir)

    if os.path.exists(merged_file):
        print(f"[!] Removing old merged file: {merged_file}")
        os.remove(merged_file)

    if os.path.exists(final_output):
        print(f"[!] Removing old final output: {final_output}")
        os.remove(final_output)

    os.makedirs(output_dir, exist_ok=True)

    # 1. Load m3u8 playlist
    print("[*] Loading m3u8 playlist...")
    playlist = m3u8.load(m3u8_url)
    segments = playlist.segments
    ts_urls = [urljoin(m3u8_url, seg.uri) for seg in segments]

    # 2. Check for encryption
    key_info = playlist.keys[0]
    if key_info and key_info.method:
        key_uri = urljoin(m3u8_url, key_info.uri)
        iv = bytes.fromhex(key_info.iv[2:]) if key_info.iv else b"\x00" * 16
        aes_key = requests.get(key_uri).content
        print(f"[+] Encryption method: {key_info.method}, key downloaded successfully.")
    else:
        print("[-] No encryption detected.")


def download_with_retry(i_url):
    i, ts_url = i_url
    local_path = os.path.join(output_dir, f"{i:05d}.ts")
    if os.path.exists(local_path):
        return

    for attempt in range(1, max_retries + 1):
        try:
            r = requests.get(ts_url, timeout=timeout_sec)
            r.raise_for_status()
            data = r.content

            if aes_key:
                cipher = AES.new(aes_key, AES.MODE_CBC, iv)
                data = cipher.decrypt(data)

            with open(local_path, "wb") as f:
                f.write(data)
            return
        except Exception as e:
            if attempt < max_retries:
                print(f"[!] Retry {attempt} for: {ts_url}")
            else:
                print(f"[✘] Failed after {max_retries} attempts: {ts_url} | Error: {e}")

def merge_ts_files():
    print("[*] Merging all .ts files into one...")
    with open(merged_file, "wb") as merged:
        for i in range(len(ts_urls)):
            ts_path = os.path.join(output_dir, f"{i:05d}.ts")
            if os.path.exists(ts_path):
                with open(ts_path, "rb") as f:
                    merged.write(f.read())
            else:
                print(f"[⚠] Missing segment: {ts_path}")

def convert_to_mp4():
    global ffmpeg_path
    if platform.system() == "Windows":
        ffmpeg_path = os.path.join(file_path, "ffmpeg", "windows","ffmpeg.exe")
        print("[*] The script is running on Windows, proceeding with conversion...")
        print("[*] Converting to MP4 using ffmpeg...")
    elif platform.system() == "Linux":
        ffmpeg_path = os.path.join(file_path, "ffmpeg", "linux","ffmpeg")
        print("[*] The script is running on Linux, proceeding with conversion...")
        print("[*] Converting to MP4 using ffmpeg...")
    elif platform.system() == "macOS":
        ffmpeg_path = os.path.join(file_path, "ffmpeg", "mac","ffmpeg")
        print("[*] The script is running on macOS, proceeding with conversion...")
        print("[*] Converting to MP4 using ffmpeg...")
    else:
        print("[✘] Unsupported platform.")
        print("[✘] Please run this script on Windows, Linux, or macOS.")
        print("[*] You can download ffmpeg from https://ffmpeg.org/download.html, and convert your video files manually.")
        return
    


    try:
        check_ffmpeg()
    except Exception as e:
        print(f"[✘] The ffmpeg executable is not found or not configured correctly: {e}")
        return
    

    os.system(f'{ffmpeg_path} -y -i "{merged_file}" -c copy "{final_output}"')
    print(f"[✔] Done. Output file: {final_output}")


if __name__ == "__main__":
    
    create_output_dir()

    print("[*] Starting concurrent download of .ts files...")
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        list(tqdm(executor.map(download_with_retry, enumerate(ts_urls)), total=len(ts_urls)))

    merge_ts_files()
    convert_to_mp4()
