# AUTOSLOP

Fully free Python script that writes, generates, edits, and uploads short AI-generated story videos to YouTube Shorts with no manual steps in between.

The script was mostly written by me but i did use ai to learn new things and help me overcome hurdles as i am a beginner to python.

Gemini writes a video prompt, Google Flow turns it into four 4-second clips with native audio, ffmpeg and moviepy clean and merge them, and UniPost publishes the finished 16-second vertical video to a connected YouTube channel.

## How it works

1. Gemini generates a prompt 
2. Google flow uses omni flash 1.1 to generate 4 clips
3. the clips get downloaded as a zip
4. the zip gets extracted and the watermark gets cleaned
5. the video gets merged together with my audio.
6. the video gets uploaded on youtube

generating free quality videos was possible only through google flows free 50 credits daily and since its api is not free, i am using pyautogui clicks.
the pyautogui clicks are harcoded and may differ from device to 

unipost allows max 100 api video uploads per month on the free plan.

i have tested this and have made a few videos on my experimental youtube channel:

https://youtube.com/@pickyourrealitytv?si=98tkUzHFgQRFBGd1
