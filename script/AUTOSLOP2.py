from google import genai
import os
import re
import sys
import time
import json
import random
import zipfile
import subprocess
import requests
import pyautogui
import pyperclip
import keyboard
import imageio_ffmpeg
from pathlib import Path
from moviepy import VideoFileClip, concatenate_videoclips

sys.stdout.reconfigure(encoding="utf-8")

start_time = time.time()
scriptfolder = Path(__file__).resolve().parent
downloads = Path.home() / "Downloads"

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
uni_key = os.getenv("UNIPOST_API_KEY")
if not uni_key:
    sys.exit("UNIPOST_API_KEY is not set")

yt_account_id = "8922450a-4035-47fa-b42e-ee70a4396267"

models = [
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
]

history_file = scriptfolder / "history.json"
history = json.loads(history_file.read_text(encoding="utf-8")) if history_file.exists() else []

pools = {
    "genre": ["cozy fantasy", "solarpunk", "gentle noir", "folk tale", "quiet science fiction", "myth", "surreal comedy", "gentle mystery", "seafaring adventure", "fable"],
    "tone": ["wonder", "melancholy", "suspense", "humor", "serenity", "awe", "warmth", "curiosity"],
    "style": ["oil painting", "claymation", "watercolor", "paper cut-out", "neon anime", "low-poly 3D", "storybook illustration", "cinematic realism", "stop-motion felt"],
    "hero": ["a small fox", "a clockwork bird", "a paper boat", "a lantern spirit", "a lone maintenance robot", "a giant snail", "a traveler seen only from behind", "a moss-covered golem", "a stray kite", "a tiny whale"],
    "setting": ["a floating market", "a desert observatory", "a flooded library", "a snowbound train station", "a coral city", "a rooftop garden above the clouds", "a canyon of mirrors", "an abandoned lighthouse", "a night bazaar", "a glacier cave"],
    "ending": ["a twist", "a loop back to the opening image", "a quiet reversal", "a small victory", "a bittersweet goodbye", "a surprising reveal"],
    "music": ["solo piano", "harp and strings", "music box", "warm synth pads", "acoustic guitar", "cello with soft percussion", "marimba and flute", "glass harmonica"],
}
pick = {key: random.choice(values) for key, values in pools.items()}

seed_block = (
    f"CREATIVE SEED (follow it, it overrides any default look): genre: {pick['genre']}; tone: {pick['tone']}; "
    f"visual style: {pick['style']}; protagonist: {pick['hero']}; setting: {pick['setting']}; "
    f"ending: {pick['ending']}; music: {pick['music']}. "
    f"Never reuse or resemble these earlier stories: {'; '.join(history[-30:]) or 'none yet'}.\n\n"
)

story_prompt = """
You are an expert short-form story director, screenwriter, cinematographer, sound designer, and AI video prompt engineer. You do NOT generate the video yourself. You write ONE complete, production-ready VIDEO GENERATION PROMPT that Google Flow's video model will use to generate a 16-second, 9:16 vertical micro-story as EXACTLY 4 separate clips, with native generated audio.

============================================================
GENERATION DIRECTIVE (HIGHEST PRIORITY, OVERRIDES EVERYTHING ELSE)
============================================================

The prompt you write MUST instruct the video generator, in strict imperative language, to:

1. Generate EXACTLY 4 (FOUR) separate video clips. Not 1, not 2, not 3, not 5, not 6.
2. Make every clip EXACTLY 4 seconds long, EXACTLY 360p, and EXACTLY 9:16 vertical. No other duration, resolution, or aspect ratio. Never 480p, 720p, 1080p, or 4K.
3. Output CLIPS ONLY: no images, storyboards, scripts, text replies, captions, thumbnails, or extra files.
4. Never stop early. If fewer than 4 clips exist, the task is INCOMPLETE; keep generating until all 4 exist, in order.
5. Deliver 4 individual, separate files. Do not combine, stitch, add, remove, extend, shorten, merge, or split any clip. No bonus, transition, outro, or end-card clips.
6. Keep native generated audio ON in every clip.

The 4 clips are:
CLIP 1 (0:00-0:04) = SETUP AND HOOK.
CLIP 2 (0:04-0:08) = DEVELOPMENT / COMPLICATION.
CLIP 3 (0:08-0:12) = TURN / CLIMAX.
CLIP 4 (0:12-0:16) = RESOLUTION AND FINAL IMAGE.

Restate "4 clips, 4 seconds each, 360p, 9:16, clips only, native audio on" inside every clip block and again in the FINAL DELIVERY REQUIREMENT.

============================================================
FLOW GENERATION SETTINGS (MANDATORY, REPRODUCE IN THE OUTPUT)
============================================================

The output must instruct the generator to configure the actual Flow UI before generating:

1. GENERATION TYPE: Video.
2. ORIENTATION: 9:16 portrait / vertical. Never leave the default, never 16:9. Verify the Flow UI shows 9:16 before generating.
3. LENGTH: exactly 4 seconds, selected in the Flow UI. Never 6, 8, or 10 seconds. Do not rely on the text prompt for duration.
4. NUMBER OF OUTPUTS: exactly 4. These are the four clip files.
5. RESOLUTION: 360p / Draft 360p whenever the selected model offers it. Never substitute 720p when 360p is available. If the model has no 360p option, do not pretend it was selected.
6. MODEL: use a model that supports 9:16, 4-second generation, the required resolution, and native audio. Do not switch models only to satisfy a different unsupported setting.
7. AUDIO: if Flow exposes an audio option, keep it enabled. Never mute.
8. FINAL UI CHECK before clicking Generate: Video, 9:16, 4 seconds, 4 outputs, 360p (when available), audio on.

These are configuration only. They must never be rendered as content inside any video.

============================================================
FILE NAMING RULE (MANDATORY, REPRODUCE IN THE OUTPUT)
============================================================

The output must instruct: after the four clips are generated, rename them in Flow: Clip 1 to exactly "clip1", Clip 2 to exactly "clip2", Clip 3 to exactly "clip3", Clip 4 to exactly "clip4". Lowercase, no spaces, no extra words. Rename only in the Flow interface. NEVER render any clip name as text inside any video.

============================================================
STORY RULES
============================================================

- The video is ONE complete micro-story with a beginning, a turn, and an ending, fully understandable with no words. One protagonist, one clear want or problem, one visible change by the end.
- Clips are generated independently but play back-to-back with NO transitions between them. Therefore each clip block must define an OPENING STATE and a CLOSING STATE, and the CLOSING STATE of clip N must match the OPENING STATE of clip N+1 exactly (same location, protagonist position and pose, time of day, lighting, weather, camera distance). The story must feel like one continuous piece.
- CONTINUITY LOCKS: write a STYLE LOCK (one visual style, palette, lens, lighting approach), a CHARACTER SHEET (protagonist described by distinctive silhouette, colors, materials, and props), and a WORLD LOCK (setting and its rules). Repeat all three VERBATIM inside every clip block so each clip is self-contained.
- IDENTITY-DRIFT PROTECTION: independent clips cannot guarantee the same face. Make the protagonist a non-human character (an animal, creature, robot, object, spirit) OR a human seen only from behind, in silhouette, or at distance. Never rely on a recognizable human face or matching facial features across clips.
- MOTION: only large, broad, whole-body actions (walking, turning, looking, raising an arm, sitting, flying, drifting). NEVER fine finger dexterity, precisely timed hand-object contact, complex choreography, crowds, or fast overlapping actions. One clear event per clip.
- DENSITY: every clip needs at least 3 continuously moving background or atmospheric elements, active cinematic camera movement (push-in, dolly, orbit, crane, parallax, low-angle reveal), and something visibly changing at least every 2 seconds. Avoid static lockoffs.
- ENDING: the last frame at 0:16 holds on a strong, screenshot-worthy image. No fade to black, no end card, no logo, no text. The ending may echo the opening image if that suits the story.
- NO TEXT: no on-screen text of any kind: no titles, subtitles, captions, logos, watermarks, or readable signs. The story is told visually and with sound.
- ADVERTISER-FRIENDLY: family-safe. No gore, sexual content, hate, self-harm, dangerous or imitable acts, real people, celebrities, brand names, logos, or copyrighted characters, worlds, or songs. Menace and sadness are allowed only in a gentle, non-graphic form.
- VARIETY: if a CREATIVE SEED or a list of earlier premises appears at the top of this message, obey it and never reuse or resemble those premises. Otherwise invent something unusual and specific. Avoid cliches: a lone figure walking into fog, a glowing orb, a mysterious door, a chosen-one plot. Vary genre, tone, setting, era, protagonist type, visual style, and ending type from video to video.

============================================================
AUDIO RULES (NATIVE GENERATED AUDIO)
============================================================

Native audio is generated by the video model in every clip. The output prompt must require, in every clip:

1. A wordless INSTRUMENTAL MUSIC BED. Describe the SAME instrument palette, tempo, key, and mood in all four clips (write an AUDIO LOCK line and repeat it verbatim in every clip block) so the four clips read as one score.
2. At least two environment-specific sound effects synced to the on-screen action.
3. NO speech, NO narration, NO dialogue, NO singing, NO lyrics, NO whispering, NO crowd voices.
4. NO silence. Music must already be playing at the first frame and still playing at the last frame of every clip, with no fade-in or fade-out at clip edges, so the joins between clips are less audible.
5. Audio intensity follows the story: lowest in clip 1, building in clip 2, peak in clip 3, resolving in clip 4.

============================================================
SELF-CHECK BEFORE WRITING THE FINAL ANSWER
============================================================

Verify: exactly 4 clips; each 4 seconds, 360p, 9:16; the directive is stated at the top, inside every clip block, and at the end; the Flow settings block and the file naming block are present; CLOSING STATE of each clip matches OPENING STATE of the next; the STYLE LOCK, CHARACTER SHEET, WORLD LOCK, and AUDIO LOCK are repeated verbatim in every clip block; the protagonist is non-human or never shown by face; no on-screen text anywhere; no speech or lyrics in the audio; content is advertiser-friendly; the ending holds with no fade. Output only a draft that passes ALL checks.

============================================================
OUTPUT FORMAT
============================================================

The FIRST line of your output must be the OVERALL TITLE line. Output ONLY the following structure, nothing else. No reasoning, no alternatives, no summary.

OVERALL TITLE: (maximum 50 characters; only letters, numbers, and spaces; no colons, quotes, or symbols; a curious, specific story title)

GENRE / PREMISE: (one sentence)

TOTAL RUNTIME: 16 seconds
ASPECT RATIO: 9:16 vertical
RESOLUTION: 360p (every clip)
AUDIO: native generated audio, wordless music + sound effects, no speech
NUMBER OF CLIPS TO GENERATE: EXACTLY 4 (FOUR), each exactly 4 seconds, 360p, 9:16. NEVER 2. NEVER 3. NEVER 5. NEVER 6.

GENERATION DIRECTIVE: (full six-point directive above, in strict imperative language addressed to the video generator)

FLOW GENERATION SETTINGS: (all eight items above, in strict imperative language)

FILE NAMING RULE: (as above, in strict imperative language)

STORY LOCKS:
STYLE LOCK:
CHARACTER SHEET:
WORLD LOCK:
AUDIO LOCK:

CLIP 1 (0:00-0:04): SETUP AND HOOK
CLIP DELIVERABLE: Clip 1 of 4. One separate video clip, exactly 4 seconds, 360p, 9:16, native audio on. Clip only. All 4 clips must be generated.
STORY BEAT:
OPENING STATE:
ACTION:
ENVIRONMENT: (at least 3 continuously moving elements)
CHARACTERS: (non-human, or seen only from behind, in silhouette, or at distance)
CAMERA:
LIGHTING:
COLOR / MATERIALS:
SOUND DESIGN: (audio lock repeated, plus at least two synced sound effects)
CLOSING STATE:
(repeat STYLE LOCK, CHARACTER SHEET, WORLD LOCK, AUDIO LOCK verbatim in this block)

CLIP 2 (0:04-0:08): DEVELOPMENT / COMPLICATION
(same fields as Clip 1; OPENING STATE must equal Clip 1's CLOSING STATE)

CLIP 3 (0:08-0:12): TURN / CLIMAX
(same fields as Clip 1; OPENING STATE must equal Clip 2's CLOSING STATE; this clip holds the single biggest visual event and the audio peak)

CLIP 4 (0:12-0:16): RESOLUTION AND FINAL IMAGE
(same fields as Clip 1; OPENING STATE must equal Clip 3's CLOSING STATE)
FINAL FRAME: (the exact screenshot-worthy image held from about 0:15.5 to 0:16, no fade, no end card, no text)

FINAL DELIVERY REQUIREMENT: (in strict imperative language addressed to the generator, restate in full: "Deliver EXACTLY 4 (FOUR) video clips: Clip 1 (0:00-0:04), Clip 2 (0:04-0:08), Clip 3 (0:08-0:12), Clip 4 (0:12-0:16). Each exactly 4 seconds, exactly 360p, exactly 9:16 vertical, native audio on. Clips only. NEVER deliver 2, 3, 5, or 6 clips. NEVER use any resolution other than 360p. If fewer than 4 clips exist, keep generating until all 4 are delivered. Name the four clips exactly clip1, clip2, clip3, clip4 in Flow so the files sort in order.")

NEGATIVE PROMPT: only 1 clip, only 2 clips, only 3 clips, 5 clips, 6 clips, more than 4 clips, fewer than 4 clips, one long combined video, clips longer than 4 seconds, clips shorter than 4 seconds, extra clips, bonus clips, alternate takes, transition clips, outro clips, end-card clips, resolution other than 360p, 480p, 720p, 1080p, 4K, horizontal aspect ratio, square aspect ratio, images instead of clips, still images, storyboards, text-only output, script output, thumbnails, silent video, muted audio, speech, narration, dialogue, singing, lyrics, whispering, crowd voices, on-screen text, subtitles, captions, titles, logos, watermarks, readable signs, clip names rendered on screen, filename labels rendered on screen, recognizable human faces, changing character appearance between clips, inconsistent art style between clips, mismatched opening and closing states between clips, fade to black, end card, black frames between clips, glitch transitions, fine finger movement, malformed hands, extra fingers, distorted faces, complex choreography, crowds, chaotic motion, static empty environments, flat lighting, boring camera movement, gore, sexual content, hate, real people, celebrities, brand names, copyrighted characters, copyrighted songs, cliche premises, repeated premises.

After the NEGATIVE PROMPT, output exactly two more lines. They are metadata for the human editor and are NOT part of the video prompt:
TAGS: (8 to 12 comma-separated lowercase tags relevant to this story; no # symbols, no quotes)
LOGLINE: (one teaser sentence about this story that does not spoil the ending)

Do not ask questions. Do not provide multiple concepts or alternatives. Do not summarize afterward. Do not include any text outside the structure above.

Create the complete production-ready 16-second, 9:16, 360p micro-story video prompt now, with native audio and EXACTLY 4 clips, each 4 seconds, clips only, never fewer or more.
"""

response = None
for model in models:
    try:
        response = client.models.generate_content(model=model, contents=seed_block + story_prompt)
        break
    except Exception:
        continue

if response is None:
    sys.exit("no model returned a response")

response_text = response.text
print(response_text)

match = re.search(r"(?im)^\W*OVERALL TITLE:\W*([^\n*]+)", response_text)
if not match:
    sys.exit("could not find a title in the response")

extracted_title = re.sub(r'[<>:"/\\|?*]', "", match.group(1))
extracted_title = re.sub(r"\s+", " ", extracted_title).strip().rstrip(".")[:60].strip()
if not extracted_title:
    sys.exit("the title came back empty")

tags_match = re.search(r"(?im)^\W*TAGS:\s*(.+)$", response_text)
logline_match = re.search(r"(?im)^\W*LOGLINE:\s*(.+)$", response_text)

if tags_match:
    tags = [t.strip().strip("*#") for t in tags_match.group(1).split(",")]
    tags = [t for t in tags if t][:12]
else:
    tags = ["shorts", "shortstory", "aivideo"]

logline = logline_match.group(1).strip().strip("*") if logline_match else extracted_title

video_prompt = re.sub(r"(?im)^\W*(TAGS|LOGLINE):.*$", "", response_text).strip()

(scriptfolder / f"{extracted_title}.txt").write_text(response_text, encoding="utf-8")

retry = "retry generating the video(s) that have failed to generate"
rename = "rename clip 1 to clip1, clip 2 to clip2, clip 3 to clip3 and clip 4 to clip4 "

pyautogui.click(650, 1051)
time.sleep(2)
pyautogui.click(739, 437)
time.sleep(5)
pyautogui.click(980, 870)
time.sleep(2)
pyautogui.click(1887, 208)
time.sleep(3)
pyautogui.click(900, 925)
pyperclip.copy(video_prompt)
pyautogui.hotkey("ctrl", "v")
time.sleep(5)
keyboard.press_and_release("enter")
time.sleep(100)
pyautogui.click(1644, 767)
time.sleep(180)
pyautogui.click(1600, 933)
pyperclip.copy(retry)
pyautogui.hotkey("ctrl", "v")
keyboard.press_and_release("enter")
time.sleep(200)
pyautogui.click(1600, 933)
pyperclip.copy(rename)
pyautogui.hotkey("ctrl", "v")
keyboard.press_and_release("enter")
time.sleep(50)
pyautogui.click(1784, 159)
time.sleep(2)
pyautogui.click(1704, 189)
time.sleep(60)

zip_file = None
for _ in range(60):
    fresh = [z for z in downloads.glob("*.zip") if z.stat().st_mtime > start_time]
    if fresh:
        zip_file = max(fresh, key=lambda z: z.stat().st_mtime)
        break
    time.sleep(5)

if zip_file is None:
    sys.exit("no new zip was downloaded")

time.sleep(5)

run_folder = scriptfolder / f"{extracted_title} {time.strftime('%Y%m%d-%H%M')}"
run_folder.mkdir(exist_ok=True)

with zipfile.ZipFile(zip_file, "r") as z:
    z.extractall(run_folder)

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
cleaned = run_folder / "cleaned"
final_dir = cleaned / "final"
final_dir.mkdir(parents=True, exist_ok=True)

for f in run_folder.iterdir():
    if f.suffix.lower() != ".mp4":
        continue
    result = subprocess.run(
        [
            ffmpeg, "-y",
            "-i", str(f),
            "-vf", "delogo=x=285:y=565:w=29:h=29:show=0",
            "-c:v", "libx264",
            "-crf", "18",
            "-preset", "medium",
            "-c:a", "aac",
            "-b:a", "192k",
            str(cleaned / f.name),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stderr)
        sys.exit(f"ffmpeg failed on {f.name}")

pattern = re.compile(r"clip([1-4])", re.I)
found = {}
for f in cleaned.glob("*.mp4"):
    m = pattern.search(f.name)
    if m:
        found[int(m.group(1))] = f

if sorted(found) != [1, 2, 3, 4]:
    sys.exit(f"expected clips 1 to 4, found {sorted(found)}")

clips = [VideoFileClip(str(found[n])) for n in (1, 2, 3, 4)]
video = concatenate_videoclips(clips)
final_path = final_dir / f"{extracted_title}.mp4"
video.write_videofile(str(final_path), codec="libx264", audio_codec="aac")
video.close()
for c in clips:
    c.close()

base = "https://api.unipost.dev/v1"
headers = {"Authorization": f"Bearer {uni_key}"}

hashtags = " ".join("#" + t.replace(" ", "") for t in tags[:3])
description = (
    f"{logline}\n\n"
    "What did you make of this one? Tell me in the comments.\n\n"
    "Made with AI. New stories every day.\n\n"
    f"#shorts #shortstory {hashtags}"
)

reserve = requests.post(
    f"{base}/media",
    headers=headers,
    timeout=60,
    json={
        "filename": final_path.name,
        "content_type": "video/mp4",
        "size_bytes": final_path.stat().st_size,
    },
)
media = reserve.json().get("data") or reserve.json()

with open(final_path, "rb") as f:
    put = requests.put(media["upload_url"], data=f, headers={"Content-Type": "video/mp4"}, timeout=600)
if put.status_code >= 300:
    sys.exit(f"media upload failed with {put.status_code}")

uploaded = False
for _ in range(30):
    info = requests.get(f"{base}/media/{media['id']}", headers=headers, timeout=60)
    body = info.json().get("data") or info.json()
    if body.get("status") == "uploaded":
        uploaded = True
        break
    time.sleep(2)

if not uploaded:
    sys.exit("media never finished uploading")

post = requests.post(
    f"{base}/posts",
    headers=headers,
    timeout=60,
    json={
        "platform_posts": [
            {
                "account_id": yt_account_id,
                "caption": description,
                "media_ids": [media["id"]],
                "platform_options": {
                    "title": extracted_title[:100],
                    "made_for_kids": False,
                    "privacy_status": "public",
                    "tags": tags,
                    "category_id": "22",
                    "contains_synthetic_media": True,
                    "shorts": True,
                },
            }
        ]
    },
)
print(post.status_code, post.text)

if post.status_code not in (201, 202):
    sys.exit("the post was rejected")

post_id = (post.json().get("data") or post.json())["id"]
status = "queued"
for _ in range(60):
    check = requests.get(f"{base}/posts/{post_id}", headers=headers, timeout=60)
    status = (check.json().get("data") or check.json()).get("status", status)
    if status not in ("queued", "publishing"):
        break
    time.sleep(5)

print(status)

with open(scriptfolder / "upload_log.txt", "a", encoding="utf-8") as log:
    log.write(f"{time.strftime('%Y-%m-%d %H:%M')} | {extracted_title} | {status}\n")

history.append(extracted_title)
history_file.write_text(json.dumps(history[-200:]), encoding="utf-8")
