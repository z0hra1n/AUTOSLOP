# AUTOSLOP

A Python script that writes, generates, edits, and uploads short AI-generated story videos to YouTube Shorts with no manual steps in between.

Gemini writes a video prompt, Google Flow turns it into four 4-second clips with native audio, ffmpeg and moviepy clean and merge them, and UniPost publishes the finished 16-second vertical video to a connected YouTube channel.

## How it works

1. Gemini generates a prompt 
2. Google flow uses omni flash 1.1 to generate 4 clips
3. the clips get downloaded as a zip
4. the zip gets extracted and the watermark gets cleaned
5. the video gets merged together with my audio.

Although this may seem repetitive and template based, i am gonna use one more script to mix things up a bit so my channel eventually does get monetized.
