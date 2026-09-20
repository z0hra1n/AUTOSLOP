# AUTOSLOP

A Python script that writes, generates, edits, and uploads short AI-generated story videos to YouTube Shorts with no manual steps in between.

Gemini writes a video prompt, Google Flow turns it into four 4-second clips with native audio, ffmpeg and moviepy clean and merge them, and UniPost publishes the finished 16-second vertical video to a connected YouTube channel.

How it works
Creative seed. Each run picks a random genre, tone, visual style, protagonist, setting, ending, and music style. It also reads history.json so it doesn't repeat recent stories.
Prompt. Gemini writes a full Flow prompt for a 9:16, 360p micro-story made of exactly four 4-second clips. If a model fails, the script falls back to the next one in the list.
Flow. pyautogui pastes the prompt into Google Flow, waits for generation, retries failed clips, renames them clip1 to clip4, and downloads the zip.
Cleanup. ffmpeg removes the watermark with a delogo filter and keeps each clip's audio.
Merge. moviepy joins the four clips in order into one video.
Upload. The video goes to the UniPost API and is published as a public YouTube Short, with the AI-generated content flag set.
Log. The final status is written to upload_log.txt and the title is added to history.json.
Requirements
Windows, with a screen that matches the click coordinates in the script
Python 3.11
A Gemini API key
Access to Google Flow, signed in and open in the browser
A UniPost account with your YouTube channel connected

Install the packages:

pip install google-genai pyautogui pyperclip keyboard imageio-ffmpeg moviepy requests

The script uses the moviepy 2.x imports, so make sure moviepy is version 2 or newer.

Setup

API keys. Set them as environment variables so they never appear in the code, then restart your terminal or editor:

setx GEMINI_API_KEY "your Gemini key"
setx UNIPOST_API_KEY "your UniPost key"

YouTube account ID. List your connected accounts and copy the id of the YouTube one into yt_account_id in the script:

curl -H "Authorization: Bearer your UniPost key" https://api.unipost.dev/v1/accounts

Click coordinates. The Flow automation clicks fixed screen positions. To find yours, run this, hover over a button, and read the printed position:

python
import pyautogui, time
time.sleep(5)
print(pyautogui.position())

Replace the values in the pyautogui.click(...) calls near the middle of the script. Keep the browser maximized, at the same zoom level and screen resolution every run.

Usage

Open Flow in your browser, then run:

python story_script.py

A full run takes roughly 10 to 15 minutes, most of it fixed waits while Flow generates the clips. Don't touch the mouse or keyboard while it runs. To stop it, move the mouse to the top-left corner of the screen.

To run it on a schedule, create a task in Windows Task Scheduler. The PC has to be on, unlocked, and showing Flow when the task fires.

Files
File	What it is
story_script.py	The whole pipeline
history.json	Titles of recent stories, created on the first run
upload_log.txt	One line per run with the time, title, and final status
<title>.txt	The full Gemini response for each run
<title> <date>/	Extracted clips, cleaned clips, and the final merged video
Customizing
Story variety. Edit the pools dictionary to change the genres, styles, protagonists, settings, endings, and music the seed picks from.
Prompt. The story_prompt string holds the full instructions Gemini uses to write the Flow prompt.
Models. The models list is the fallback order for Gemini.
Watermark. The delogo box is set in the ffmpeg command. Adjust x, y, w, and h if your clips are a different size.
Description. The description template and the tags are built near the end of the script.
Limitations
The Flow steps depend on screen coordinates and fixed waits, so a change to the Flow interface, your screen, or generation time can break a run.
Each clip's audio is generated separately, so you may hear small changes at the 4-second joins.
Independent clips can't guarantee the same character, so the prompt uses non-human protagonists or characters seen from behind.
UniPost's free plan allows 100 posts per month. Its docs also note that Google can force uploads from an unverified API project to private, so check the first upload's visibility in YouTube Studio.
The script exits without posting if the title can't be read, no new zip is downloaded, clips 1 to 4 aren't all present, or ffmpeg or the upload fails.
Content notes

Every video is AI-generated. The description says so, and the upload sets YouTube's synthetic media flag. Follow YouTube's policies on AI-generated content and monetization, and check Google Flow's terms before running this unattended.

Security

Never commit API keys. Keep history.json, upload_log.txt, the saved prompt files, and the run folders out of the repository with a .gitignore.
