from google import genai
import os
import re
import sys
import base64
import time
import pyautogui# type: ignore
import pyperclip # type: ignore
import keyboard# type: ignore
from pathlib import Path
import zipfile
import subprocess
import imageio_ffmpeg # type: ignore
import requests
from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips # type: ignore


sys.stdout.reconfigure(encoding='utf-8')
apikey = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=apikey)

models = ["gemini-3.8-flash",
          "gemini-3.7-flash",
          "gemini-3.6-flash",
          "gemini-3.5-flash",
          "gemini-3.5-flash-lite"]

with open("prompt.txt", encoding="utf-8") as f:
    prompt = f.read()

for model in models:
     try:
          response = client.models.generate_content(
     model =model,
     contents=prompt
)
          
          break

     except Exception:
          pass


print(response.text)

response_text = response.text

match = re.search(r'(?i)TITLE:\s*\**\s*([^\n*]+)', response_text)
if match:
    extracted_title = match.group(1).strip()

    # Remove characters Windows doesn't allow in filenames
    extracted_title = re.sub(
        r'[<>:"/\\|?*]',
        '',
        extracted_title
    ).strip().rstrip('.')

    if not extracted_title:
        extracted_title = "UNKNOWN_TITLE"

    output_filename = f"{extracted_title}.txt"

    with open(output_filename, "w", encoding="utf-8") as file:
        file.write(response.text)

else:
    extracted_title = "UNKNOWN_TITLE"
    print("WARNING: could not extract title. Raw response above.")

video_prompt = response.text



retry = "retry generating the video(s) that have failed to generate"
rename = "rename clip 1 to clip1, clip 2 to clip2, clip 3 to clip3 and clip 4 to clip4 "
    

# may differ for different devices

pyautogui.click(650,1051)
time.sleep(2)
pyautogui.click(739,437)
time.sleep(5)
pyautogui.click(980,870)
time.sleep(2)
pyautogui.click(1887,208)
time.sleep(3)
pyautogui.click(900,925)
pyperclip.copy(video_prompt)
pyautogui.hotkey("ctrl", "v")
time.sleep(5)
keyboard.press_and_release('enter')
time.sleep(100)
pyautogui.click(1644,767)
time.sleep(180)
pyautogui.click(1600,933)
pyperclip.copy(retry)
pyautogui.hotkey("ctrl", "v")
keyboard.press_and_release('enter')
time.sleep(200)
pyautogui.click(1600,933)
pyperclip.copy(rename)
pyautogui.hotkey("ctrl", "v")
keyboard.press_and_release('enter')
time.sleep(50)
pyautogui.click(1784,159)
time.sleep(2)
pyautogui.click(1704,189)
time.sleep(60)

downloads = Path.home() / "Downloads"


zips = sorted(
    downloads.glob("*.zip"),
    key=lambda x: x.stat().st_mtime,
    reverse=True
)

scriptfolder = Path(__file__).resolve().parent

zip_file = zips[0]

output_dir = scriptfolder / extracted_title
output_dir.mkdir(exist_ok=True)

with zipfile.ZipFile(zip_file, "r") as z:
    z.extractall(output_dir)

latestoutput = extracted_title

time.sleep(5)
 
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
 
# Watermark box (x, y, w, h) — adjust if resolution differs
X, Y, W, H = 565, 1131, 65, 59
 
SRC_DIR = output_dir
OUT_DIR = SRC_DIR / "cleaned"
OUT_DIR.mkdir(exist_ok=True)
FINAL_DIR = OUT_DIR / "final"
FINAL_DIR.mkdir(exist_ok=True)
 
mp4_files = [f for f in SRC_DIR.iterdir() if f.suffix.lower() == ".mp4"]

for f in mp4_files:
    out_path = OUT_DIR / f.name

    cmd = [
        FFMPEG, "-y",
        "-i", str(f),
        "-vf", "delogo=x=285:y=565:w=29:h=29:show=0",
        "-c:v", "libx264",
        "-crf", "18",
        "-preset", "medium",
        "-an",
        str(out_path),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

pat = re.compile(r"clip([1-4])", re.I)

found = {}

for f in OUT_DIR.glob("*.mp4"):

    m = pat.search(f.name)

    if m:
        found[int(m.group(1))] = f.name

clip1, clip2, clip3, clip4 = found[1], found[2], found[3], found[4]

clips = [VideoFileClip(str(OUT_DIR / c )) for c in (clip1,clip2,clip3,clip4)]
video = concatenate_videoclips(clips)

audio = AudioFileClip(str(scriptfolder / "audio.mp3"))
audio = audio.subclipped(0,(min(audio.duration,video.duration)))

video = video.with_audio(audio)
video.write_videofile(str(FINAL_DIR / f"{extracted_title}.mp4"), codec="libx264", audio_codec="aac")

UNI_KEY = os.getenv("UNIPOST_KEY")
YT_ACCOUNT_ID = "8922450a-4035-47fa-b42e-ee70a4396267"

TITLE = f"{extracted_title} (COMMENT YOUR CHOICE)"
DESCRIPTION = """
Which reality would you pick? Comment your number 👇

Made with AI. New worlds every day. Subscribe to choose your reality.

#shorts #chooseyourreality
"""
TAGS = ["choose your reality", "would you rather", "aivideo", "shorts", "shortstory"]


scriptfolder = Path(__file__).resolve().parent
video = scriptfolder / extracted_title / "cleaned" / "final" / f"{extracted_title}.mp4"

BASE = "https://api.unipost.dev/v1"
HEAD = {"Authorization": f"Bearer {UNI_KEY}"}
j = lambda r: r.json().get("data") or r.json()

media = j(requests.post(f"{BASE}/media", headers=HEAD, json={
    "filename": video.name, "content_type": "video/mp4", "size_bytes": video.stat().st_size}))

with open(video, "rb") as f:
    requests.put(media["upload_url"], data=f, headers={"Content-Type": "video/mp4"}, timeout=600)

for _ in range(30):
    if j(requests.get(f"{BASE}/media/{media['id']}", headers=HEAD)).get("status") == "uploaded":
        break
    time.sleep(2)

r = requests.post(f"{BASE}/posts", headers=HEAD, timeout=60, json={
    "platform_posts": [{
        "account_id": YT_ACCOUNT_ID,
        "caption": DESCRIPTION,
        "media_ids": [media["id"]],
        "platform_options": {
            "title": TITLE[:100],
            "made_for_kids": False,
            "privacy_status": "public",
            "tags": TAGS,
            "category_id": "22",
            "contains_synthetic_media": True,
            "shorts": True,
        },
    }]})
print(r.status_code, r.text)


