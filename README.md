# AUTOSLOP

This is the automation script I use to turn a simple idea into a finished AI-generated YouTube Short.

The basic idea is pretty simple: Gemini comes up with the video prompt, Google Flow generates the clips, and the Python script takes care of the boring parts afterwards.

Right now the videos follow a fixed format: 16 seconds, 9:16 vertical, 5 choices, but only 4 actual video files.

How it works

Gemini
  ↓
video prompt
  ↓
Google Flow
  ↓
4 clips
  ↓
download + extract
  ↓
FFmpeg cleanup
  ↓
merge clips + add music
  ↓
final video
  ↓
YouTube upload

The 4 clips

The five choices are packed into four clips like this:

0:00 - 0:04   Hook
0:04 - 0:06   Option 1
0:06 - 0:08   Option 2
0:08 - 0:12   Option 3
0:12 - 0:14   Option 4
0:14 - 0:16   Option 5

So:

clip1 = hook

clip2 = option 1 + option 2

clip3 = option 3

clip4 = option 4 + option 5

The clips are renamed in Flow before they are downloaded so the script doesn't have to guess which one came first.

What the script does

1. Generates the prompt

Gemini is used to write the actual production prompt for the video.

The prompt contains all the rules for the video, including the timeline, clip count, aspect ratio, visual style, text, and the five choices.

The script also tries several Gemini models if one of them fails.

2. Controls Google Flow

There isn't a Flow API being used here. Instead, the script controls the browser using pyautogui, keyboard, and the clipboard.

It opens Flow, pastes the generated prompt, starts generation, waits for the result, retries failed generations, and tells Flow to rename the clips.

Because this is screen automation, the browser needs to be in roughly the same position/layout the script expects.

3. Finds the downloaded ZIP

Flow downloads the generated clips as a ZIP.

The script looks in the Downloads folder and picks the newest ZIP, then extracts it into a folder named after the generated video title.

4. Cleans the clips

FFmpeg is used through imageio-ffmpeg.

At the moment, this includes removing the small watermark from the generated clips.

The cleaned clips are placed in:

<video title>/
└── cleaned/
    ├── clip1.mp4
    ├── clip2.mp4
    ├── clip3.mp4
    └── clip4.mp4

5. Puts everything together

The script finds clip1 through clip4, loads them in that order, and concatenates them with MoviePy.

It then loads audio.mp3, trims it to the length of the video, and adds it to the final result.

The finished video ends up here:

<video title>/
└── cleaned/
    └── final/
        └── <video title>.mp4

6. Uploads the video

The final MP4 can then be uploaded through UniPost.

The current setup publishes it as a YouTube Short with a title, description, tags, and the synthetic-media setting enabled.

Requirements

You'll need:

Python 3.10+

Google Gemini API access

Google Flow access

A browser that can run Flow

Windows (the current automation is written around Windows)

audio.mp3 in the same folder as the script

Install the Python dependencies with:

pip install google-genai pyautogui pyperclip keyboard imageio-ffmpeg requests moviepy

API key

Gemini reads the API key from an environment variable:

GEMINI_API_KEY

For PowerShell:

$env:GEMINI_API_KEY="your-api-key"

If you are putting this project on GitHub, don't put the actual key in the code.

The same goes for the UniPost credentials and YouTube account ID.

Running it

Once everything is set up:

python main.py

Then the automation takes over.

The exact amount of time it takes depends mostly on how long Flow takes to generate the clips.

A couple of things to know

Flow automation is fragile

The Flow part uses screen coordinates rather than an API.

That means changing things like:

screen resolution

Windows display scaling

browser zoom

browser window position

Flow's UI

can break the automation.

If a click suddenly lands somewhere completely wrong, this is probably why.

Clip names matter

The editing stage looks for:

clip1
clip2
clip3
clip4

So if Flow doesn't rename them correctly, the script won't know the intended order.

Watermark coordinates are fixed

The FFmpeg delogo filter currently uses fixed coordinates.

If the generated video resolution or watermark position changes, those coordinates will need to be changed too.

Project structure

A normal run looks roughly like this:

project/
├── main.py
├── audio.mp3
├── README.md
│
└── <generated title>/
    ├── ...
    └── cleaned/
        └── final/
            └── <generated title>.mp4

Why I made it this way

The annoying part of making these videos isn't really generating one video. It's everything around it.

Getting the prompt right, making sure Flow actually produces all four clips, figuring out which downloaded file is which, cleaning them, putting them together in the right order, adding the music, and finally uploading the result adds up very quickly.

This script is basically an attempt to make all of that one pipeline.

It's still very much a work in progress, especially the Flow automation, but the goal is for the only real creative input to be the idea for the next "choose your reality" video.
