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

for model in models:
     try:
          response = client.models.generate_content(
     model =model,
     contents="""
You are an expert short-form video director, screenwriter, cinematographer, visual storyteller, sound designer, and AI video prompt engineer specializing in viral "choose your reality" hypothetical-choice ranking videos for AI video generators such as Gemini Omni Flash.

Your job is NOT to generate the video itself. Your job is to generate ONE complete, production-ready VIDEO GENERATION PROMPT that another AI video generator (Gemini Omni Flash) can directly use.

The concept should feel like a viral TikTok/Reels/Shorts "choose your reality" video: beautiful, surreal, cinematic, instantly understandable, increasingly insane, emotionally compelling, and designed around visual curiosity, retention, escalation, and shareability.

NUMBER OF CLIPS TO GENERATE: EXACTLY 4 (FOUR) — each exactly 4 seconds, each 360p, each 9:16 vertical. NEVER 2. NEVER 3. NEVER 5. NEVER 6.

FLOW GENERATION SETTINGS — CONFIGURE THE ACTUAL FLOW UI BEFORE GENERATING:

Before generating any video, use the actual Google Flow video-generation controls and explicitly configure the generation settings to match the requirements below.

FILE NAMING RULE (MANDATORY): After the four clips are generated in Flow, rename them inside Flow so the names sort in clip order: rename Clip 1 to exactly "clip1", Clip 2 to exactly "clip2", Clip 3 to exactly "clip3", and Clip 4 to exactly "clip4". Use these exact lowercase names with no spaces, no extra words, and no punctuation. The renaming is done only in the Flow interface; the prompt text submitted to the video model does not need to start with any label. NEVER render any clip name as text inside any video. The only on-screen text allowed remains the ON-SCREEN TEXT / ON-SCREEN TITLE strings. THIS RULE MUST BE REPRODUCED INSIDE THE FINAL OUTPUT (see OUTPUT FORMAT).

STATE CLEARLY IN THE PROMPT (these seven items MUST be reproduced in the final output inside the FLOW GENERATION SETTINGS block described in OUTPUT FORMAT):

1. GENERATION TYPE:
   - Video

2. VIDEO ORIENTATION / ASPECT RATIO:
   - 9:16 PORTRAIT / VERTICAL
   - Do not leave the aspect ratio at the default.
   - Do not use 16:9 landscape.
   - Verify that the Flow UI visibly reflects the 9:16 / portrait setting before generating.

3. GENERATION LENGTH:
   - EXACTLY 4 SECONDS
   - Select the 4-second generation-length option in the Flow UI.
   - Do not rely on the text prompt alone to determine duration.
   - Do not select 6 seconds, 8 seconds, 10 seconds, or any other available duration.

4. NUMBER OF OUTPUTS:
   - EXACTLY 4 OUTPUTS
   - If Flow provides a number-of-outputs control, set it to 4 before generating.
   - The four outputs are the four required clip files.
   - Do not use the number-of-outputs setting to represent the five options. There are exactly four deliverable files.

5. RESOLUTION:
   - USE 360p / DRAFT 360p when the selected Flow model exposes that resolution option.
   - Do not substitute 720p when 360p is available.
   - If the selected model does not provide a 360p option, do not pretend that 360p was selected. Keep the required 9:16 portrait orientation and 4-second duration.

6. MODEL:
   - Use the video model appropriate for this task and verify that it supports 9:16 portrait, 4-second generation, and the required resolution before generating.
   - Do not switch models merely to satisfy a different unsupported setting.

7. FINAL UI VERIFICATION:
   Before clicking Generate, verify the actual Flow controls show:
   - Video
   - 9:16 portrait
   - 4 seconds
   - 4 outputs
   - 360p when available

These UI settings have priority over any default Flow settings.

IMPORTANT:
The instructions above control the actual Flow generation configuration. The creative prompt below controls what appears inside the generated videos. Do not treat the UI configuration requirements as visual content to be rendered inside the videos.

============================================================

GENERATION DIRECTIVE — HIGHEST PRIORITY — OVERRIDES EVERYTHING ELSE IN THIS PROMPT

============================================================

The video-generation prompt you write will be handed to Gemini Omni Flash. That prompt MUST instruct Gemini Omni Flash, strictly and unambiguously, to do the following and nothing else:

1. GENERATE EXACTLY 4 (FOUR) SEPARATE VIDEO CLIPS. Not 1. Not 2. Not 3. Not 5. Not 6. EXACTLY FOUR.

2. EVERY ONE OF THE 4 CLIPS MUST BE EXACTLY 4 SECONDS LONG. Four clips x 4 seconds = 16 seconds total. Do not generate 8-second clips, 2-second clips, 5-second clips, 6-second clips, or one 16-second video.

3. EVERY ONE OF THE 4 CLIPS MUST BE 360p RESOLUTION AND 9:16 VERTICAL YOUTUBE-SHORTS OR TIKTOK OR INSTAGRAM REEL STYLE. Not 480p. Not 720p. Not 1080p. Not 4K. Not any other resolution. Not any other aspect ratio, Not 16:9, Not widescreen.

4. THE DELIVERABLE IS CLIPS ONLY. The generator must output four video clips and nothing else: no still images, no storyboards, no written scripts, no text descriptions of clips, no explanations, no summaries, no captions, no audio-only files, no thumbnails, no preview frames, no extra videos.

5. THE GENERATOR MUST NEVER GENERATE ONLY 2 CLIPS. Under no circumstances may the generator stop after 2 clips, produce a 2-clip result, or merge the 4 clips down into 2 clips. If it has produced fewer than 4 clips, the task is INCOMPLETE and it must keep generating until all 4 clips exist. If it can only produce a limited number of clips per generation call, it must continue with further generation calls until all 4 are delivered, in order, each one 4 seconds and 360p.

6. THE 4 CLIPS ARE FIXED AND ORDERED:
CLIP 1 = 0:00–0:04 = HOOK / INTRO ONLY (one 4-second, 360p clip).
CLIP 2 = 0:04–0:08 = ONE SINGLE 4-second, 360p clip file containing Option 1 (first 2 seconds) hard-cut into Option 2 (last 2 seconds).
CLIP 3 = 0:08–0:12 = ONE SINGLE 4-second, 360p clip containing Option 3 (full 4 seconds).
CLIP 4 = 0:12–0:16 = ONE SINGLE 4-second, 360p clip file containing Option 4 (first 2 seconds) hard-cut into Option 5 (last 2 seconds).

7. THE FIVE OPTIONS DO NOT EQUAL FIVE CLIPS. There are 5 options but only 4 clips. Option 1 and Option 2 live inside the SAME single clip (Clip 2). Option 4 and Option 5 live inside the SAME single clip (Clip 4). Do NOT generate the options as separate clips. Do NOT generate 5 clips. Do NOT generate 6 clips (hook + 5 options). Do NOT generate 2 clips (for example, one clip for "options 1 and 2" and one clip for "options 4 and 5"). The count is FOUR, always.

8. THE 4 CLIPS MUST BE DELIVERED AS 4 INDIVIDUAL, SEPARATE FILES, NOT combined into one long video and NOT stitched by the generator. The human editor will stitch them.

9. THE GENERATOR MUST NOT ADD, REMOVE, EXTEND, SHORTEN, MERGE, OR SPLIT ANY CLIP. Each clip is exactly 4 seconds. No bonus clips. No transition clips. No outro clips. No end-card clips. No alternate takes.

The final prompt you output MUST open with a GENERATION DIRECTIVE block (see OUTPUT FORMAT) that states all nine points above in strict, imperative language, and MUST repeat the "4 clips, 4 seconds each, 360p, 9:16, clips only, never 2 clips" requirement inside every clip block and again at the very end of the prompt.

============================================================

CORE FORMAT — MANDATORY

============================================================

The final video is EXACTLY 16 SECONDS LONG, 9:16 VERTICAL, RESOLUTION 360p, with EXACTLY 5 PRIMARY OPTIONS/CHOICES, delivered as EXACTLY 4 SEPARATE 4-SECOND 360p VIDEO CLIPS.

THE FOLLOWING TIMELINE IS ABSOLUTE, FIXED, AND NON-NEGOTIABLE:

0:00–0:04 = HOOK / INTRO ONLY. THIS IS NOT AN OPTION.
0:04–0:06 = OPTION 1.
0:06–0:08 = OPTION 2.
0:08–0:12 = OPTION 3.
0:12–0:14 = OPTION 4.
0:14–0:16 = OPTION 5.

THESE SIX TIME WINDOWS ARE THE ACTUAL VIDEO STRUCTURE.

DO NOT reinterpret them. DO NOT merge them. DO NOT reorder them. DO NOT shorten them. DO NOT extend them. DO NOT add extra option footage. DO NOT remove any option footage. DO NOT create an additional transition segment. DO NOT create an outro segment. DO NOT create an end card. DO NOT create a seventh section. DO NOT treat CLIP 1 as an option.

CLIP STRUCTURE (EXACTLY FOUR CLIPS, EACH 4 SECONDS, EACH 360p, EACH 9:16):

CLIP 1 = 0:00–0:04 = HOOK / INTRO ONLY

CLIP 2 = 0:04–0:08 = ONE SINGLE 4-SECOND GENERATED FILE containing:

0:04–0:06 = OPTION 1
0:06–0:08 = OPTION 2

CLIP 3 = 0:08–0:12 = ONE SINGLE CONTINUOUS 4-SECOND VIDEO CLIP containing:

0:08–0:12 = OPTION 3

CLIP 4 = 0:12–0:16 = ONE SINGLE 4-SECOND GENERATED FILE containing:

0:12–0:14 = OPTION 4
0:14–0:16 = OPTION 5

CLIP COUNT LOCK: THERE ARE EXACTLY FOUR CLIPS. THE GENERATOR MUST NEVER PRODUCE TWO CLIPS. THE GENERATOR MUST NEVER PRODUCE SIX CLIPS. A CLIP CONTAINING TWO OPTIONS (CLIP 2 AND CLIP 4) IS STILL ONE CLIP, NOT TWO.

THIS DISTINCTION IS CRITICAL — AND IT IS THE OPPOSITE OF A MORPHING SHOT:

CLIP 2 and CLIP 4 must each be authored so that their two halves are INDISTINGUISHABLE FROM TWO SEPARATELY FILMED CLIPS SPLICED TOGETHER BY AN EDITOR. This is intentional: the output will be cut together by a human editor afterward, and the boundary must never try to disguise itself as one continuous take.

OPTION 1 AND OPTION 2 MUST EXIST SEQUENTIALLY IN TIME INSIDE THE SAME 4-SECOND FILE, BUT MUST NOT SHARE CAMERA MOTION, LIGHTING STATE, OR SOUND ACROSS THE BOUNDARY.

OPTION 4 AND OPTION 5 MUST EXIST SEQUENTIALLY IN TIME INSIDE THE SAME 4-SECOND FILE, BUT MUST NOT SHARE CAMERA MOTION, LIGHTING STATE, OR SOUND ACROSS THE BOUNDARY.

THEY MUST NOT APPEAR SIDE-BY-SIDE. THEY MUST NOT APPEAR IN A SPLIT SCREEN. THEY MUST NOT APPEAR AS TWO PANELS. THEY MUST NOT APPEAR SIMULTANEOUSLY.

THE VISUAL WORLD OF OPTION 1 HARD-CUTS INTO THE VISUAL WORLD OF OPTION 2 AT EXACTLY 0:06.

THE VISUAL WORLD OF OPTION 4 HARD-CUTS INTO THE VISUAL WORLD OF OPTION 5 AT EXACTLY 0:14.

The viewer should be able to watch Clip 2 from 0:04 to 0:08 and perceive it as two separate shots edited together, not one evolving shot. The viewer should be able to watch Clip 4 from 0:12 to 0:16 and perceive it the same way.

============================================================

GLOBAL RULES — APPLY TO ALL FOUR GENERATED CLIPS

============================================================

EVERY CLIP MUST BE 360P.

INSTRUCT THE AI CLEARLY, REPEATEDLY, AND IN STRICT IMPERATIVE LANGUAGE TO GENERATE EXACTLY 4 (FOUR) CLIPS, EACH EXACTLY 4 SECONDS LONG, EACH AT 360p RESOLUTION, EACH 9:16 VERTICAL. THE AI MUST OUTPUT CLIPS ONLY (NO IMAGES, NO TEXT, NO SCRIPTS, NO EXPLANATIONS). THE AI MUST NEVER GENERATE ONLY 2 CLIPS, AND MUST NEVER STOP BEFORE ALL 4 CLIPS ARE DELIVERED. THE AI MUST NEVER USE ANY RESOLUTION OTHER THAN 360p.

Every clip must independently contain enough information to be generated correctly without relying on hidden context from another clip.

Every clip must preserve the same overall concept, cinematic quality, visual storytelling language, typography philosophy, sound philosophy, and escalation logic.

GLOBAL VISUAL STYLE must explicitly include:

"9:16 vertical aspect ratio", "360p", and "dreamy, surreal"

The overall visual language must feel like premium cinematic fantasy advertising rather than generic AI-generated footage.

The imagery should be beautiful, surreal, cinematic, highly polished, visually dense, emotionally appealing, instantly understandable, and optimized for short-form retention.

Every clip must feel like part of the same 16-second video while still having a clearly distinct environment, palette, atmosphere, architecture, composition, and surreal identity.

Do not make the four clips look like unrelated videos in concept or premise. Do not make the five options look like variations of the same scene.

============================================================

GLOBAL TYPOGRAPHY AND TEXT STYLE — MANDATORY FOR ALL CLIPS

============================================================

Typography is a GLOBAL VISUAL RULE and must be carried consistently across every clip.

All on-screen text must be physically rendered INSIDE the generated footage itself.

Text must NEVER look like a generic editing-software overlay pasted on top of the video.

Every text element must visually belong to the world in which it appears.

The typography must be designed according to the environment's architecture, culture, materials, atmosphere, era, lighting, color palette, geometry, perspective, depth, physical surfaces, and visual mood.

The font family, letter shapes, weight, spacing, scale, texture, material, depth, reflections, glow, shadows, beveling, transparency, surface treatment, perspective, and lighting must all feel native to the environment.

Typography may appear as: architectural lettering, carved lettering, illuminated signage, engraved metal, glowing glass, embossed stone, projected light, holographic environmental lettering, painted surfaces, luminous particles forming letters, physically existing signage, magical environmental typography, or another environment-appropriate physical treatment.

The exact words specified in ON-SCREEN TEXT or ON-SCREEN TITLE fields must be visibly generated. The generator must NOT invent additional words, alter spelling, duplicate text, replace text with random symbols, create fake unreadable pseudo-writing, or warp letters until illegible.

Text must remain highly readable, short, bold, high-contrast, correctly spelled, and visually integrated. Text must never cover the primary subject or the most important visual event, and must never appear during the wrong timeline window.

TITLE MATERIAL RULE (MANDATORY): Because every clip is rendered at 360p, all hook text and option titles must be placed on stable, flat or gently curved, clearly lit physical surfaces or in clear open air: carved, painted, engraved, embossed, illuminated signage, lit letters, or solid luminous lettering. All text must be plain, readable capital letters in the exact spelling given. NEVER render any text as runes, glyphs, sigils, symbols, alien script, or any decorative pseudo-alphabet. NEVER place text behind, under, or inside water, glass, ice, smoke, fog, heat haze, or any refractive, rippling, or distorting layer. NEVER place text on a surface that is rotating, rippling, or moving quickly. NEVER build letters from particles, sparks, or dust that could scatter and lose legibility. If the environment is wet, glassy, or turbulent, place the title on a dry, solid, still surface within that environment (for example a brass plaque, a stone slab, a wooden sign, or a luminous sign floating in clear space).

============================================================

GLOBAL TRANSITION PHILOSOPHY — MANDATORY (ABRUPT / SPLICE-STYLE)

============================================================

CLIP 2 and CLIP 4 are each generated as ONE 4-second file, but the boundary at 0:06 and at 0:14 must function as a HARD, ABRUPT, INSTANT CUT — as if two independently filmed clips were edited together in post.

At the boundary:

Camera position, angle, lens, and framing must reset completely and instantly. NO shared camera motion may cross the boundary.
Lighting must reset completely and instantly. NO gradual lighting evolution may cross the boundary.
The environment must change completely and instantly to the new option's world. NO partial reveal, dissolve, or overlap of the old and new environment is allowed.
Music and ambience must stop completely at the boundary and a distinct new musical/ambient bed for the next option must begin cleanly at frame one of the new half — exactly like a cut between two separate source files.
The subject/character may reappear in a new pose, new framing, and new lighting state with no requirement of physical continuity from the prior half.

Think:

OPTION A ──── HARD CUT ──── OPTION B

NOT:

OPTION A ──── continuous visual evolution ──── OPTION B

FORBIDDEN at the 0:06 and 0:14 boundaries: morphing, dissolving, cross-fading, camera carry-through, lighting carry-through, matched motion, portals or environmental unfolding used as a bridge, or any mechanism designed to make the two halves feel like one continuous take. The two halves should read as two separate clips even though they are delivered as one file.

IMPORTANT: "two separate clips" here describes only how the two halves must LOOK AND SOUND to the viewer. It does NOT change the file count. Clip 2 remains ONE 4-second file and Clip 4 remains ONE 4-second file. The total number of generated clips remains EXACTLY FOUR.

============================================================

GLOBAL MOTION RULES — STRICT

============================================================

Every physical action any character performs must be a large, broad, whole-body or whole-arm gross-motor movement: walking, turning, looking around, raising an arm, broad gesturing, sitting, slowly reaching, standing while the environment moves around them.

NEVER include: fine finger dexterity, precisely timed hand-object contact, tiny hand movements, complex choreography, multiple simultaneous complex transformations, fast overlapping choreography, multiple characters performing different actions simultaneously, rapid transformations, complex facial acting.

If an object must be touched, cut away immediately before or after the exact touch, or keep the contact off-frame.

One clean, unmistakable visual "wow" event per option is enough. Do not overload an option with competing transformations.

For CLIP 2 and CLIP 4, each half's movement is self-contained to that half only — motion does NOT need to (and should NOT) carry forward across the 0:06 or 0:14 boundary, since the boundary is a hard cut, not a continuation.

CHARACTER CONTINUITY RULE (MANDATORY): Every option is generated as an independent shot, so character identity CANNOT carry across options, and across the hard cuts at 0:06 and 0:14 in particular. NEVER write "the same character", "the same passenger", "the same person", or any wording that requires a character to look identical in another option. Each option's CHARACTERS field must describe either (a) a character seen only from behind, in silhouette, or at a distance where identity does not matter, or (b) no character at all. Do not require recognizable faces, matching outfits, or matching identities anywhere in the video.

============================================================

GLOBAL ENVIRONMENTAL DENSITY — STRICT

============================================================

No clip may ever feel static, sparse, empty, or visually dead.

Every clip/option's ENVIRONMENT field must describe at least THREE independently moving background or atmospheric elements running continuously throughout its duration (e.g. drifting particles, petals, dust, mist, glowing pulsing light, moving reflections, drifting clouds, swaying structures, floating debris, shimmering water, orbiting celestial bodies, magical particles, atmospheric haze, moving shadows, flowing fabric, floating objects).

Something in frame must visibly intensify, brighten, grow, expand, reveal, or accelerate at least once every 2 seconds. The video should feel like it is constantly building rather than plateauing. This escalation should become increasingly strong toward Option 5.

Camera movement must remain active within each half. Favor push-ins, slow dolly movement, controlled crane movement, orbiting, parallax, aerial descent, aerial rise, low-angle reveals, foreground reveals, environmental reveals. Avoid fully static lockoffs.

For CLIP 2 and CLIP 4, each half's camera movement is independent and self-contained — it does not need to set up or lead into the next half, since the cut is abrupt.

============================================================

GLOBAL LIGHTING RULES

============================================================

Use cinematic volumetric lighting: god rays, atmospheric haze, glowing practical lights, rim lighting, luminous skies, reflections, subtle bloom, volumetric particles, environmental light sources.

Lighting richness must evolve with escalation across the five options. Option 5 receives the richest lighting design in the video.

For CLIP 2 and CLIP 4, each half's lighting is a fresh, independent design appropriate to its own world. Lighting must reset completely at the 0:06 and 0:14 boundaries — no gradual shift, no shared light source, no carried-over color temperature.

============================================================

GLOBAL SOUND DESIGN RULES

============================================================

Every clip/option must contain: (1) a dreamy musical layer, (2) at least two environmental sounds specific to that setting, (3) one transition/whoosh/shimmer accent.

Sound must feel cinematic and physically connected to the environment. Sound intensity should increase toward Option 5.

For CLIP 2 and CLIP 4, sound must behave as TWO SEPARATE AUDIO EVENTS, not one continuous one. The music and ambience for the first half must stop completely at the boundary (0:06 or 0:14), and a distinct new musical/ambient bed for the second half must start cleanly at the top of that half — exactly like an edit between two separate source clips. Do not evolve one musical layer across the boundary. Do not carry ambience across the boundary.

============================================================

ABSOLUTE TIMELINE INTERPRETATION RULE

============================================================

When the prompt says "OPTION 1 (0:04–0:06)" it means OPTION 1 is the visual state occupying the FIRST TWO SECONDS of CLIP 2. When the prompt says "OPTION 2 (0:06–0:08)" it means OPTION 2 is the visual state occupying the SECOND TWO SECONDS of CLIP 2.

It does NOT mean generate Option 1 and Option 2 as two independently rendered files, place both options on screen simultaneously, or use a title card, black frame, or fade-to-black between them.

Instead: GENERATE CLIP 2 AS ONE 4-SECOND, 360p FILE. Within that file, 0:04–0:06 is Option 1's fully self-contained world, and at the 0:06 mark the file abruptly and completely cuts to Option 2's fully self-contained world for 0:06–0:08. The cut itself consumes zero runtime — it is instantaneous, like a normal edit point, not a dissolve or effect.

The exact same principle applies to Option 4 and Option 5 at the 0:14 mark: CLIP 4 is ONE 4-SECOND, 360p FILE.

Therefore the generator must NEVER output Option 1 and Option 2 as two clips, and must NEVER output Option 4 and Option 5 as two clips. Doing so would produce the wrong clip count.

============================================================

BOUNDARY RULES — EXTREMELY STRICT

============================================================

At exactly 0:04, the hook ends and Option 1 begins. At exactly 0:06, Option 1 hard-cuts into Option 2. At exactly 0:08, Option 2 ends and Option 3 begins. At exactly 0:12, Option 3 ends and Option 4 begins. At exactly 0:14, Option 4 hard-cuts into Option 5. At exactly 0:16, the video ends.

The 0:06 boundary and the 0:14 boundary ARE meant to read as ordinary hard edits — this is required, not a flaw to avoid. There SHOULD be a visible, instantaneous change in camera position, lens, framing, lighting, and environment at 0:06 and 0:14.

FORBIDDEN at these boundaries: a slow dissolve, a crossfade, a morph, a portal-style bridge, a matched-motion whip-pan used to disguise the cut as continuous, camera carry-through, lighting carry-through, or any device intended to make the viewer feel the two halves are one uninterrupted shot.

Also still forbidden, as in any well-made cut: a black frame, a white flash, a glitch effect, a generic wipe, a slideshow effect, or a visible title/transition card. The cut should look like a clean, professional, ordinary edit — instant and complete, but not gimmicky.

============================================================

CONCEPT — NOT A RIGID "CHOOSE YOUR ___" TEMPLATE

============================================================

Do not force the concept into "CHOOSE YOUR {{CATEGORY}}" phrasing. Instead invent or adapt the theme hint into any compelling hypothetical scenario built around a choice. Examples:

"YOU'RE HOME ALONE. CHOOSE YOUR HOUSE." "YOU AND YOUR BROTHER GET TELEPORTED TO ANOTHER DIMENSION. CHOOSE YOUR DIMENSION." "YOU INHERIT A MYSTERIOUS HOTEL. WHICH ROOM ARE YOU TAKING?" "YOU WAKE UP WITH $1 BILLION AND NO RULES. WHAT ARE YOU BUILDING?"

Invent a similarly strong premise. It must be instantly understandable within the first few seconds, create a genuine choice, allow five dramatically different visual options, and become increasingly surreal, desirable, and spectacular.

HOOK TEXT COMPRESSION: The premise may be as rich as the examples above, but the hook text that is physically rendered in the footage must be a compressed form of the premise of MAXIMUM 6 WORDS (for example "CHOOSE YOUR HOUSE" or "WHICH ROOM ARE YOU TAKING?"). The rest of the premise must be communicated visually by the establishing shot, not by additional rendered words.

============================================================

THE HOOK — CLIP 1 — MOST IMPORTANT RULE

============================================================

CLIP 1 must occupy EXACTLY 0:00–0:04, is the HOOK/INTRO, and is NOT OPTION 1. CLIP 1 must contain ZERO option-choice content and must establish the hypothetical situation only. CLIP 1 is its own separate 4-second, 360p clip file.

CLIP 1 must be the MOST BEAUTIFUL AND ATTENTION-GRABBING VISUAL IN THE ENTIRE VIDEO from its very first frame. No slow build, no calm establishing shot, no gradual reveal. The viewer's first reaction must be "what am I looking at?" while grasping the basic premise within 1–2 seconds.

Use an extraordinary establishing shot (an impossible mansion floating above an ocean, a portal opening above a city, a bedroom suspended inside a galaxy, a staircase leading into space, an impossible luxury environment, or another extraordinary cinematic fantasy environment).

CLIP 1 must contain the primary on-screen hook text — short, bold, extremely readable, immediately explaining the premise, physically rendered and integrated into the environment. The hook text MUST BE A MAXIMUM OF 6 WORDS, because longer text becomes illegible at 360p, and it must follow the TITLE MATERIAL RULE.

============================================================

CLIP 2 — FIRST TWO OPTION REVEALS (HARD-CUT PAIR)

============================================================

CLIP 2 = 0:04–0:08, delivered as ONE 4-second, 360p file containing two fully self-contained, hard-cut option segments. It is ONE clip, not two.

TIMELINE: 0:04–0:06 = OPTION 1 / 0:06–0:08 = OPTION 2.

OPTION 1: Appealing but relatively believable — the "reasonable" entry point. Fully established by 0:04, runs as its own self-contained shot through 0:06.

OPTION 2: Noticeably more imaginative and surreal than Option 1. Begins as a completely fresh shot — new camera, new lighting, new environment — at exactly 0:06.

Each option has its own short on-screen title, and its own distinct environment, palette, atmosphere, lighting, composition, surreal-technique combination, and emotional mood.

CLIP 2 CUT: State plainly that the boundary at 0:06 is an abrupt hard cut — describe the last camera/lighting state of Option 1 and the first camera/lighting state of Option 2 as two independent setups with no shared element. Do NOT describe any morphing, dissolving, portal, or camera-carry-through mechanism.

DO NOT: split-screen, picture-in-picture, side-by-side reveal, montage with a soft crossfade, morph, or continuous camera-through mechanism. A clean, ordinary hard cut is REQUIRED here — do not soften it.

============================================================

CLIP 3 — CENTRAL OPTION REVEAL

============================================================

CLIP 3 = 0:08–0:12. This is ONE continuous 4-second, 360p shot containing ONLY Option 3, which receives the full 4 seconds as a single continuous scene. Option 3 must be highly surreal and represent a major escalation from Options 1 and 2. Use the extra time for the camera to travel through or around the environment, building toward one major visual "wow" event. Do not split Option 3 into sub-options or introduce a sixth option. The handoff from Option 2 at 0:08 is a normal hard cut into a new clip, matching the same abrupt style as the other boundaries.

============================================================

CLIP 4 — FINAL TWO OPTION REVEALS (HARD-CUT PAIR)

============================================================

CLIP 4 = 0:12–0:16, delivered as ONE 4-second, 360p file containing two fully self-contained, hard-cut option segments. It is ONE clip, not two.

TIMELINE: 0:12–0:14 = OPTION 4 / 0:14–0:16 = OPTION 5.

OPTION 4: Extraordinary. Fully established by 0:12, runs as its own self-contained shot through 0:14.

OPTION 5: The ultimate jaw-dropping choice — the clear reward for watching to the end. Begins as a completely fresh shot — new camera, new lighting, new environment — at exactly 0:14. Option 5 must receive the strongest visual, lighting, sound, surrealism, scale, emotional impact, and shareability treatment in the video.

CLIP 4 CUT: State plainly that the boundary at 0:14 is the most spectacular HARD CUT in the video — describe Option 4's final self-contained setup and Option 5's brand-new opening setup as two independent shots with zero shared camera motion, lighting, or sound. The abruptness itself should heighten anticipation and impact. Do NOT describe any morphing, dissolving, portal-bridge, or camera-carry-through mechanism.

There must be: NO black frame, NO generic crossfade, NO wipe, NO glitch, NO title card, NO loss of clarity — just a clean, powerful, instantaneous edit.

The final 0.5–1 second must become a screenshot-worthy composition.

============================================================

OPTION TITLES — MANDATORY

============================================================

Every option must have a short on-screen title: ALL CAPS, 2–5 words, bold, high-contrast, instantly readable, specific, visually integrated. Pair the option number with the actual name when appropriate, e.g. "OPTION 1: THE BEACH HOUSE." The title itself must only contain the exact words intended for the viewer, physically rendered inside the generated video, following the GLOBAL TYPOGRAPHY rules and the TITLE MATERIAL RULE (no runes, glyphs, or symbols; no text behind water, glass, or other distorting layers; no text on moving or rotating surfaces).

Exact timing: OPTION 1 TITLE = 0:04–0:06 / OPTION 2 TITLE = 0:06–0:08 / OPTION 3 TITLE = 0:08–0:12 / OPTION 4 TITLE = 0:12–0:14 / OPTION 5 TITLE = 0:14–0:16.

Never display an option title during another option's time window. The title change at each boundary should be just as abrupt as the visual cut — the old title disappears completely and the new title appears fresh, with no shared transition treatment.

============================================================

DREAMLIKE VISUAL LANGUAGE

============================================================

Every option must contain at least THREE simultaneous surreal/dreamlike techniques, and no two options may reuse the exact same combination. Possible techniques include: impossible scale, floating architecture, gravity-defying objects, upside-down environments, portals, miniature worlds, gigantic everyday objects, liquid flowing upward, floating islands, glowing bioluminescence, iridescent materials, pastel dreamscape skies, hyper-saturated cinematic colors, glowing particles, drifting petals, magical dust, slow-motion bubbles, bending or melting architecture, impossible reflections, multiple moons, celestial objects close to the environment, clouds inside buildings, waterfalls flowing upward, doors opening into impossible spaces, objects dissolving into harmless magical particles, folding or unfolding environments. The techniques must be active and visually apparent throughout, not a single static detail.

TECHNIQUE EXCLUSIVITY RULE (MANDATORY): The following dominant techniques may each be used in only ONE option across the whole video: (1) zero-gravity or weightless floating of a character or bed/furniture, (2) open-roof or open-to-sky/open-to-space architecture, (3) upside-down environments, (4) liquid or water contained inside architecture. Two options may never share any of these. This is in addition to the rule that no two options may reuse the same combination of techniques.

============================================================

VISUAL SEPARATION

============================================================

Every option must differ from every other option in environment, architecture, palette, atmosphere, lighting, camera composition, dominant surreal technique, and emotional mood. Never create five variations of the same room or environment, and never reuse the same surreal-technique combination. For CLIP 2 and CLIP 4, the two halves should be as visually distinct as any two unrelated clips in the video — there is no requirement (and no benefit) to sharing spatial or cinematic continuity between them, since the cut is abrupt by design.

BACKDROP EXCLUSIVITY RULE (MANDATORY): Nebulae, starfields, galaxies, and other cosmic-space backdrops may appear ONLY in Clip 1 (the hook) and in Option 5, and in NO other option. More generally, any other dominant backdrop type (for example ocean, sky, forest, city, desert, ice, or machinery) may be the dominant background of only ONE option. Two options may not share a dominant color palette either (for example, two options dominated by purple/violet).

============================================================

FOUR DISTINCT CLIPS — NOT ONE CLIP REPEATED — NEVER TWO CLIPS

============================================================

This prompt describes FOUR SEPARATE video-generation outputs: CLIP 1 (0:00–0:04), CLIP 2 (0:04–0:08), CLIP 3 (0:08–0:12), CLIP 4 (0:12–0:16). Each is exactly 4 seconds, exactly 360p, exactly 9:16.

CLIP 2 is one 4-second file containing Option 1 hard-cut into Option 2. CLIP 4 is one 4-second file containing Option 4 hard-cut into Option 5. There are FOUR clips total. There are NOT six clips. There are NOT five clips. There are NEVER two clips. The generator must NEVER output only 2 clips, must NEVER combine the four clips into two clips, and must NEVER stop before all four clips have been generated and delivered.

The generator's output is CLIPS ONLY: four video files, and nothing else.

Each clip's ACTION, ENVIRONMENT, CHARACTERS, CAMERA, COLOR/MATERIALS, LIGHTING, SOUND, TEXT, and TRANSITION fields must independently and fully describe a self-contained scene, such that if a clip block were handed to the video generator with zero other context, it would not be confused with another clip.

For CLIP 2 and CLIP 4, explicitly describe the abrupt hard-cut mechanism at the boundary — state plainly that camera, lighting, environment, and sound all reset instantly and completely, and that no element bridges the two halves.

============================================================

MANDATORY SELF-CHECK BEFORE WRITING THE FINAL ANSWER

============================================================

Before outputting the final prompt, verify ALL of the following:

Exactly 5 options exist and exactly 1 hook exists.
The six exact time windows match the timeline above.
CLIP 1 is hook-only.
CLIP 2 is exactly ONE 4-second file containing Option 1 hard-cut into Option 2.
CLIP 3 is exactly ONE 4-second shot containing Option 3.
CLIP 4 is exactly ONE 4-second file containing Option 4 hard-cut into Option 5.
The final prompt instructs the generator to produce EXACTLY 4 clips — not 2, not 3, not 5, not 6 — and this is stated in the GENERATION DIRECTIVE, inside every clip block, and in the closing FINAL DELIVERY REQUIREMENT.
The final prompt explicitly forbids generating only 2 clips, and explicitly states that generation is incomplete until all 4 clips exist.
The final prompt states that every one of the 4 clips is exactly 4 seconds, exactly 360p, and exactly 9:16 vertical, and forbids every other resolution (including 480p, 720p, 1080p, and 4K).
The final prompt states that the deliverable is CLIPS ONLY — no images, storyboards, scripts, text replies, captions, or extra files.
The final prompt states that the 5 options do NOT equal 5 clips, and that Options 1+2 share one clip and Options 4+5 share one clip.
The final prompt contains the FLOW GENERATION SETTINGS block with all seven items, and the FILE NAMING RULE block, both placed immediately after the GENERATION DIRECTIVE.
The FILE NAMING RULE block instructs the Flow agent to rename the four clips exactly clip1, clip2, clip3, clip4.
The hook ON-SCREEN TEXT is a maximum of 6 words.
No ON-SCREEN TEXT or ON-SCREEN TITLE uses runes, glyphs, symbols, or particle-built letters, and none is placed behind or under water, glass, smoke, or any distorting layer, or on a moving or rotating surface.
No CHARACTERS field uses the words "the same" to link a character to another option; every character is seen from behind, in silhouette, at a distance, or absent.
Nebula, starfield, galaxy, or cosmic-space backdrops appear only in Clip 1 and Option 5.
Zero-gravity floating, open-roof/open-to-sky architecture, upside-down environments, and liquid contained inside architecture each appear as a dominant technique in at most ONE option.
No two options share a dominant backdrop type or dominant color palette.
Option 1 and Option 2 are sequential and never simultaneous; same for Option 4 and Option 5.
The 0:06 and 0:14 boundaries are described as abrupt, instantaneous hard cuts — NOT continuous morphs, dissolves, or portal-bridges.
No camera motion, lighting state, or music/ambience is described as carrying across the 0:06 or 0:14 boundary.
No split-screen, picture-in-picture, or simultaneous-option presentation exists anywhere.
No black frame, title card, generic wipe, glitch, or slideshow effect is inserted at any boundary.
Every option contains at least 3 simultaneous dreamlike/surreal techniques, active throughout its duration.
No two options share the same surreal-technique combination, environment, palette, or camera composition.
Options escalate in visual beauty, surrealism, desirability, scale, emotional impact, and shareability, with Option 5 clearly the strongest.
Every clip/option has at least 3 continuously moving environmental or atmospheric elements, with something intensifying at least once every 2 seconds.
Every clip has active cinematic camera movement within its own segment.
Every clip/option has a dreamy musical layer, at least two environment-specific sounds, and a transition/whoosh/shimmer accent, with Clip 2 and Clip 4 each containing two separate audio events, not one continuous one.
Every required on-screen phrase is physically rendered in the footage, environment-matched, short, correctly spelled, high-contrast, readable, and never covering the main subject.
No structural label (e.g. "CLIP 1", "OPTION 2 (0:06–0:08)") ever leaks into an ON-SCREEN TEXT or ON-SCREEN TITLE field.
All four clip blocks independently describe their own setting, palette, framing, motion, and wow-event.
Option 5 ends on the strongest frame in the entire video, and the final frame holds with no fade, end card, or logo.
The video ends at exactly 0:16.
Only output a draft that passes ALL checks.

============================================================

TEXT — WHAT MAY AND MAY NOT APPEAR ON SCREEN

============================================================

Only two kinds of text are allowed to physically render in the video: (1) the exact string in the CLIP 1 "ON-SCREEN TEXT" field, and (2) the exact string in each option's "ON-SCREEN TITLE" field. No subtitles, extra UI, logos, watermarks, or extra words. All text must be clean, correctly spelled, readable, environment-integrated, and never cover the main subject. Do not treat these fields as instructions for a later editor — the exact words must actually appear in the generated footage.

============================================================

CRITICAL — DO NOT LEAK STRUCTURAL LABELS INTO THE VIDEO

============================================================

Headings such as "CLIP 1," "INTRO HOOK," "THE HOOK," "CLIP 2," "OPTION 1 (0:04–0:06)," "CLIP 4," timestamps, section dividers, timeline labels, generation-call labels, and organizational headings exist ONLY for the human reader and render pipeline. They are NEVER dialogue or text for the video generator to display. When writing each ON-SCREEN TEXT / ON-SCREEN TITLE field, write ONLY the literal words the viewer should see.

The same applies to the GENERATION DIRECTIVE, FLOW GENERATION SETTINGS, FILE NAMING RULE, CLIP DELIVERABLE, and FINAL DELIVERY REQUIREMENT fields: they are instructions to the generator about what files to produce, and they must NEVER be rendered as on-screen text in any clip. The clip names (clip1, clip2, clip3, clip4) in particular are used only to name the output files and must never appear inside any video.

============================================================

ENDING

============================================================

Option 5 occupies EXACTLY 0:14–0:16 and must be the strongest visual in the entire video. At 0:14, the viewer experiences an abrupt hard cut from Option 4 into Option 5. From approximately the final 0.5–1 second of the video, the camera and scene settle into the final screenshot-worthy composition while preserving the visual richness of the world. The final frame must hold — NO fade to black, end card, logo, outro, new text, additional choice, cut to black, or generic end screen. The final visible frame at exactly 0:16 must still be Option 5.

============================================================

OUTPUT FORMAT

============================================================

Internally invent the concept, all five options, their titles, escalation order, distinct surreal-technique combinations, and exact hard-cut descriptions for Clip 2 and Clip 4 before writing anything. Run the full self-check above. Then output ONLY the following structure, nothing else. Do NOT output reasoning, alternatives, or a summary afterward.

OVERALL TITLE:

CATEGORY / HYPOTHETICAL:

TOTAL RUNTIME: 16 seconds

ASPECT RATIO: 9:16 vertical

RESOLUTION: 360p (every clip)

NUMBER OF CLIPS TO GENERATE: EXACTLY 4 (FOUR) — each exactly 4 seconds, each 360p, each 9:16 vertical. NEVER 2. NEVER 3. NEVER 5. NEVER 6.

GENERATION DIRECTIVE (MANDATORY — MUST APPEAR AS THE FIRST INSTRUCTION BLOCK IN THE OUTPUT, WRITTEN IN STRICT IMPERATIVE LANGUAGE ADDRESSED DIRECTLY TO THE VIDEO GENERATOR): Must state, in full and without shortening, all of the following:
- "Generate EXACTLY 4 (FOUR) separate video clips. Not 1, not 2, not 3, not 5, not 6. Exactly four."
- "Every clip must be EXACTLY 4 seconds long, EXACTLY 360p resolution, and EXACTLY 9:16 vertical. Do not use 480p, 720p, 1080p, 4K, or any other resolution. Do not use any other aspect ratio. Do not use any other duration."
- "Output CLIPS ONLY. Do not output images, storyboards, scripts, text descriptions, captions, explanations, summaries, thumbnails, audio-only files, or any other non-clip content."
- "NEVER generate only 2 clips. NEVER stop after 2 clips. NEVER merge the four clips into two clips. If fewer than 4 clips have been generated, the task is INCOMPLETE — continue generating until all 4 clips exist, in order, each 4 seconds and 360p."
- "The 4 clips are: CLIP 1 (0:00–0:04) hook only; CLIP 2 (0:04–0:08) one single file containing Option 1 for its first 2 seconds hard-cut into Option 2 for its last 2 seconds; CLIP 3 (0:08–0:12) one single file containing Option 3 for its full 4 seconds; CLIP 4 (0:12–0:16) one single file containing Option 4 for its first 2 seconds hard-cut into Option 5 for its last 2 seconds."
- "There are 5 options but only 4 clips. Do not generate one clip per option. Option 1 and Option 2 share Clip 2. Option 4 and Option 5 share Clip 4. Do not split them into separate clips. Do not generate a separate clip for the hook plus five more clips for the options."
- "Deliver the 4 clips as 4 individual, separate files. Do not combine them into one long video. Do not add, remove, extend, shorten, merge, or split any clip. No bonus clips, no transition clips, no outro clips, no end-card clips, no alternate takes."
- "Any on-screen text visible inside the clips must be only the exact strings specified in the ON-SCREEN TEXT and ON-SCREEN TITLE fields — never the words of these instructions."

FLOW GENERATION SETTINGS (MANDATORY — MUST APPEAR IMMEDIATELY AFTER THE GENERATION DIRECTIVE, WRITTEN IN STRICT IMPERATIVE LANGUAGE ADDRESSED DIRECTLY TO THE VIDEO GENERATOR): Must state, in full and without shortening, all seven items from the "STATE CLEARLY IN THE PROMPT" list above: (1) generation type Video; (2) 9:16 portrait/vertical, never left at the default, never 16:9, verified visibly in the Flow UI; (3) generation length exactly 4 seconds selected in the Flow UI, never relying on the text prompt alone, never 6, 8, or 10 seconds; (4) exactly 4 outputs, which are the four clip files and never a representation of the five options; (5) 360p / Draft 360p whenever the selected model exposes it, never substituting 720p, and never pretending 360p was selected if the model does not offer it; (6) a model verified to support 9:16 portrait, 4-second generation, and 360p, never switched merely to satisfy a different unsupported setting; (7) a final UI verification before clicking Generate that Video, 9:16 portrait, 4 seconds, 4 outputs, and 360p (when available) are all visibly set. State that these UI settings have priority over any default Flow settings and that they are configuration only and must never be rendered as content inside any video.

FILE NAMING RULE (MANDATORY — MUST APPEAR IMMEDIATELY AFTER THE FLOW GENERATION SETTINGS, WRITTEN IN STRICT IMPERATIVE LANGUAGE ADDRESSED DIRECTLY TO THE VIDEO GENERATOR): Must state, in full and without shortening: "After the four clips are generated, rename them in Flow: rename Clip 1 to exactly 'clip1', Clip 2 to exactly 'clip2', Clip 3 to exactly 'clip3', and Clip 4 to exactly 'clip4'. Use these exact lowercase names with no spaces and no extra words. Do the renaming only in the Flow interface. NEVER render any clip name as text inside any video. The only on-screen text allowed remains the ON-SCREEN TEXT / ON-SCREEN TITLE strings."

GLOBAL VISUAL STYLE: Must explicitly state "9:16 vertical aspect ratio," "360p," and "dreamy, surreal." Must describe the global cinematic visual language, global typography philosophy (including the TITLE MATERIAL RULE), global text integration rules, global motion language, global environmental density, global lighting language, global sound philosophy, escalation philosophy, and the requirement that CLIP 2 and CLIP 4 each contain two segments separated by an ABRUPT HARD CUT that reads as two spliced-together clips, not a continuous morph — while remaining ONE 4-second file each.

TIMELINE CONFIRMATION: 0:00–0:04 = HOOK / INTRO ONLY 0:04–0:06 = OPTION 1 0:06–0:08 = OPTION 2 0:08–0:12 = OPTION 3 0:12–0:14 = OPTION 4 0:14–0:16 = OPTION 5 — delivered as exactly 4 clips: 0:00–0:04 / 0:04–0:08 / 0:08–0:12 / 0:12–0:16.

CLIP 1 (0:00–0:04) — INTRO HOOK

CLIP DELIVERABLE: Clip 1 of 4. Generate this as one separate video clip, exactly 4 seconds, exactly 360p, 9:16 vertical. Clip only — no images or text output. This is not a 2-clip job; all 4 clips must be generated.

IMPORTANT CLIP STRUCTURE: One continuous 4-second hook shot. Not an option. Does not contain Option 1.

ON-SCREEN TEXT: (MAXIMUM 6 WORDS, exact literal words only.)

ACTION:

ENVIRONMENT: Must contain ≥3 continuously moving environmental elements.

SURREAL ELEMENTS: Must contain ≥3 simultaneously active surreal/dreamlike techniques.

CHARACTERS: (Seen only from behind, in silhouette, at a distance, or none. Never "the same" as any other option.)

CAMERA:

LIGHTING:

COLOR / MATERIALS:

SOUND DESIGN:

TRANSITION: Describe the hard cut from the hook into Option 1 at 0:04 — no shared camera, lighting, or sound carries forward.

TEXT INTEGRATION: Describe exactly how the required hook text is physically rendered in the scene, including environment-matched font style, material, lighting, placement, perspective, depth, and readability, on a stable, clearly lit surface or in clear open air, following the TITLE MATERIAL RULE.

CLIP 2 (0:04–0:08) — ONE 4-SECOND FILE, TWO HARD-CUT OPTIONS

CLIP DELIVERABLE: Clip 2 of 4. Generate this as ONE single video clip file, exactly 4 seconds, exactly 360p, 9:16 vertical. This one file contains both Option 1 and Option 2 — it is NOT two clips. Clip only — no images or text output. Never generate only 2 clips in total; all 4 clips must be generated.

CRITICAL TIMELINE: 0:04–0:06 = OPTION 1 / 0:06–0:08 = OPTION 2

CRITICAL INSTRUCTION: This block is delivered as one 4-second file, but the two options inside it must be authored as two fully independent, self-contained shots joined by an ABRUPT HARD CUT at 0:06. No morph. No dissolve. No shared camera motion, lighting, or sound across the boundary.

OPTION 1 (0:04–0:06)

ON-SCREEN TITLE:

ACTION:

ENVIRONMENT: Must contain ≥3 continuously moving elements.

SURREAL ELEMENTS: Must contain ≥3 techniques used continuously and actively.

CHARACTERS: (Seen only from behind, in silhouette, at a distance, or none. Never "the same" as any other option.)

CAMERA:

LIGHTING:

COLOR / MATERIALS:

SOUND DESIGN:

TRANSITION: Describe the hard cut at 0:06 — state plainly that camera position, lighting, environment, and sound all reset instantly and completely into Option 2's independent setup. Do NOT describe a morph, dissolve, or camera-carry-through.

TEXT INTEGRATION: Describe exactly how the option title is physically rendered in the scene, including environment-matched font style, material, lighting, placement, perspective, depth, and readability, on a stable, clearly lit surface or in clear open air, following the TITLE MATERIAL RULE.

OPTION 2 (0:06–0:08)

ON-SCREEN TITLE:

ACTION:

ENVIRONMENT: Must contain ≥3 continuously moving elements.

SURREAL ELEMENTS: Must contain ≥3 techniques used continuously and actively, different from Option 1.

CHARACTERS: (Seen only from behind, in silhouette, at a distance, or none. Never "the same" as any other option.)

CAMERA:

LIGHTING:

COLOR / MATERIALS:

SOUND DESIGN:

TRANSITION: Confirm this half begins as a completely fresh shot at 0:06 — new camera, new lighting, new score — with no element inherited from Option 1. This is the second half of the same 4-second file but must read as a separate clip.

TEXT INTEGRATION: Describe exactly how the option title is physically rendered in the scene, including environment-matched font style, material, lighting, placement, perspective, depth, and readability, on a stable, clearly lit surface or in clear open air, following the TITLE MATERIAL RULE.

CLIP 3 (0:08–0:12) — SINGLE OPTION REVEAL

CLIP DELIVERABLE: Clip 3 of 4. Generate this as one separate video clip, exactly 4 seconds, exactly 360p, 9:16 vertical. Clip only — no images or text output. Never generate only 2 clips in total; all 4 clips must be generated.

IMPORTANT CLIP STRUCTURE: One continuous 4-second shot containing ONLY Option 3.

OPTION 3 (0:08–0:12)

ON-SCREEN TITLE:

ACTION:

ENVIRONMENT: Must contain ≥3 continuously moving elements.

SURREAL ELEMENTS: Must contain ≥3 techniques, using a combination different from Options 1 and 2.

CHARACTERS: (Seen only from behind, in silhouette, at a distance, or none. Never "the same" as any other option.)

CAMERA:

LIGHTING:

COLOR / MATERIALS:

SOUND DESIGN:

TRANSITION: Describe the hard cut from Option 2 at 0:08 into this clip — a clean, ordinary edit, not a bridge.

TEXT INTEGRATION: Describe exactly how the option title is physically rendered in the scene, including environment-matched font style, material, lighting, placement, perspective, depth, and readability, on a stable, clearly lit surface or in clear open air, following the TITLE MATERIAL RULE.

CLIP 4 (0:12–0:16) — ONE 4-SECOND FILE, TWO HARD-CUT OPTIONS

CLIP DELIVERABLE: Clip 4 of 4. Generate this as ONE single video clip file, exactly 4 seconds, exactly 360p, 9:16 vertical. This one file contains both Option 4 and Option 5 — it is NOT two clips. Clip only — no images or text output. Never generate only 2 clips in total; all 4 clips must be generated, and this is the final clip.

CRITICAL TIMELINE: 0:12–0:14 = OPTION 4 / 0:14–0:16 = OPTION 5

CRITICAL INSTRUCTION: This block is delivered as one 4-second file, but the two options inside it must be authored as two fully independent, self-contained shots joined by the most spectacular ABRUPT HARD CUT in the video at 0:14. No morph. No dissolve. No shared camera motion, lighting, or sound across the boundary.

OPTION 4 (0:12–0:14)

ON-SCREEN TITLE:

ACTION:

ENVIRONMENT: Must contain ≥3 continuously moving elements.

SURREAL ELEMENTS: Must contain ≥3 techniques used continuously and actively, extraordinary and different from earlier options.

CHARACTERS: (Seen only from behind, in silhouette, at a distance, or none. Never "the same" as any other option.)

CAMERA:

LIGHTING:

COLOR / MATERIALS:

SOUND DESIGN:

TRANSITION: Describe the hard cut at 0:14 — state plainly that camera, lighting, environment, and sound all reset instantly and completely into Option 5's independent setup. This must be the most impactful cut in the video precisely because it is abrupt, not because it bridges smoothly.

TEXT INTEGRATION: Describe exactly how the option title is physically rendered in the scene, including environment-matched font style, material, lighting, placement, perspective, depth, and readability, on a stable, clearly lit surface or in clear open air, following the TITLE MATERIAL RULE.

OPTION 5 (0:14–0:16) — FINAL PEAK

ON-SCREEN TITLE:

ACTION:

ENVIRONMENT: Must contain ≥3 continuously moving elements.

SURREAL ELEMENTS: Must contain ≥3 techniques used continuously and actively, strongest combination in the video.

CHARACTERS: (Seen only from behind, in silhouette, at a distance, or none. Never "the same" as any other option.)

CAMERA:

LIGHTING:

COLOR / MATERIALS:

SOUND DESIGN:

TRANSITION: Confirm this half begins as a completely fresh, brand-new shot at 0:14 — new camera, new lighting, new score — with nothing inherited from Option 4, then describe how the camera settles into the strongest final composition by 0:16.

TEXT INTEGRATION: Describe exactly how the option title is physically rendered in the scene, using the most spectacular environment-matched typography treatment while remaining highly readable and following the TITLE MATERIAL RULE (solid, stable, clearly lit letters; never particle-built letters).

FINAL FRAME: Describe the exact screenshot-worthy hard-hold image visible from approximately the final 0.5–1 second through 0:16.

ENDING: Confirm hard hold, no fade, no end card, no logo, no outro, and confirm the final visible frame is Option 5 at exactly 0:16.

ESCALATION LOGIC: Briefly explain how each option becomes more surreal, beautiful, desirable, spectacular, emotionally impactful, and shareable in sequence and why Option 5 is the strongest.

FINAL DELIVERY REQUIREMENT (MANDATORY — THE LAST INSTRUCTION BLOCK BEFORE THE NEGATIVE PROMPT, WRITTEN IN STRICT IMPERATIVE LANGUAGE ADDRESSED DIRECTLY TO THE VIDEO GENERATOR): Must restate in full: "Deliver EXACTLY 4 (FOUR) video clips — Clip 1 (0:00–0:04), Clip 2 (0:04–0:08), Clip 3 (0:08–0:12), Clip 4 (0:12–0:16). Each clip is exactly 4 seconds, exactly 360p, exactly 9:16 vertical. Clips only. NEVER deliver only 2 clips. NEVER deliver 5 or 6 clips. NEVER use any resolution other than 360p. If fewer than 4 clips exist, keep generating until all 4 are delivered. The 5 options live inside the 4 clips: Options 1 and 2 share Clip 2, Option 3 fills Clip 3, Options 4 and 5 share Clip 4. Name the four clips exactly clip1, clip2, clip3, clip4 in Flow so the files sort in order."

NEGATIVE PROMPT:

only 2 clips, two clips only, 2-clip output, stopping after 2 clips, merging four clips into two clips, only 1 clip, only 3 clips, 5 clips, 6 clips, more than 4 clips, fewer than 4 clips, one clip per option, separate clip for each option, Option 1 and Option 2 as separate clips, Option 4 and Option 5 as separate clips, single 16-second video, one long combined video, clips longer than 4 seconds, clips shorter than 4 seconds, 8-second clips, 2-second clips, extra clips, bonus clips, alternate takes, transition clips, outro clips, end-card clips, resolution other than 360p, 480p, 720p, 1080p, 4K, HD, Full HD, upscaled resolution, images instead of clips, still images, storyboards, text-only output, script output, written descriptions instead of clips, thumbnails, audio-only output, fine finger movement, malformed hands, extra fingers, distorted faces, inconsistent characters, duplicate characters, confusing object interactions, complex choreography, tiny actions, unreadable text, misspelled text, random letters, warped typography, text covering the main subject, subtitles, logos, watermarks, UI elements, generic environments, repeated environments, repeated surreal techniques, flat lighting, flat compositions, weak opening, slow first frame, boring camera movement, excessive camera shake, chaotic motion, multiple competing transformations, visually similar options, low-detail environments, photorealistic blandness, non-dreamy environments, static empty environments with no background motion, weak final option, weak final frame, fade to black, end card, abrupt ending with no hard hold, horizontal aspect ratio, square aspect ratio, incorrect timing, incorrect timeline, more than five choices, fewer than five choices, unclear hypothetical premise, options that do not escalate in spectacle, Option 5 weaker than earlier options, morphing transition at 0:06, morphing transition at 0:14, dissolve transition at option boundaries, continuous camera carry-through between options, shared lighting state across an option boundary, shared music bed across an option boundary, portal or environmental-unfold used to disguise a cut as continuous, split-screen options, simultaneous options, side-by-side options, picture-in-picture options, extra options, sixth option, outro footage, extra end screen, generic caption overlays, default fonts, environment-inappropriate fonts, text pasted over footage, floating text with no environmental integration, unreadable environmental text, instruction text rendered on screen, clip labels rendered on screen, black frames between options, white frames between options, generic wipes, slideshow transitions, glitch transitions, transition segment consuming option runtime, extra transition footage, runes, glyphs, sigils, symbols used as letters, alien script, pseudo-alphabet lettering, text behind water, text under water, text behind glass, text behind smoke or fog, text distorted by refraction or ripples, text on rotating surfaces, text on moving surfaces, text built from particles or sparks, hook text longer than 6 words, "the same character" across options, identity continuity across options, recognizable repeated face across options, repeated nebula backdrop, nebula in more than two clips, cosmic backdrop in options 1 to 4, two options with zero-gravity floating, two options open to the sky, two options with the same dominant color palette, two options with the same dominant backdrop, clip1 rendered on screen, clip2 rendered on screen, clip3 rendered on screen, clip4 rendered on screen, clip names rendered on screen, filename label rendered on screen.

Do not ask questions. Do not provide multiple concepts or alternatives. Do not summarize afterward. Do not include any text outside the structure above.

Create the complete production-ready 16-second, 5-option, 9:16 vertical, 360p "choose your reality" video prompt now — one that instructs the video generator to produce EXACTLY 4 clips (each 4 seconds, each 360p, clips only, never 2 clips).

REMEMBER THE EXACT TIMELINE: 0:00–0:04 = HOOK / INTRO, NOT AN OPTION 0:04–0:06 = OPTION 1 0:06–0:08 = OPTION 2 0:08–0:12 = OPTION 3 0:12–0:14 = OPTION 4 0:14–0:16 = OPTION 5

THIS TIMELINE OVERRIDES ANY OTHER INTERPRETATION.

CLIP 2 = ONE 4-SECOND FILE: OPTION 1 HARD-CUT TO OPTION 2. CLIP 4 = ONE 4-SECOND FILE: OPTION 4 HARD-CUT TO OPTION 5.

OPTION 1 → OPTION 2 MUST BE AN ABRUPT, COMPLETE HARD CUT — NOT A CONTINUOUS MORPH. OPTION 4 → OPTION 5 MUST BE AN ABRUPT, COMPLETE HARD CUT — NOT A CONTINUOUS MORPH.

EACH HALF MUST LOOK AND SOUND LIKE AN INDEPENDENTLY FILMED CLIP.

REMEMBER THE EXACT CLIP COUNT: EXACTLY 4 CLIPS. EACH 4 SECONDS. EACH 360p. EACH 9:16. CLIPS ONLY. NEVER 2 CLIPS. NEVER 6 CLIPS. THE 5 OPTIONS FIT INSIDE THE 4 CLIPS.

GLOBAL TYPOGRAPHY MUST BE ENVIRONMENT-MATCHED AND PHYSICALLY RENDERED. ALL REQUIRED TEXT MUST ACTUALLY APPEAR IN THE GENERATED FOOTAGE. NO STRUCTURAL LABELS MAY LEAK INTO THE VIDEO.

THE HOOK TEXT IS A MAXIMUM OF 6 WORDS. NO RUNES, GLYPHS, OR SYMBOLS. NO TEXT BEHIND WATER OR GLASS. NO "THE SAME" CHARACTER ACROSS OPTIONS. COSMIC BACKDROPS ONLY IN CLIP 1 AND OPTION 5. EACH DOMINANT TECHNIQUE (FLOATING, OPEN-TO-SKY, UPSIDE-DOWN, CONTAINED LIQUID) IN ONLY ONE OPTION.

AFTER GENERATION, RENAME THE CLIPS IN FLOW EXACTLY clip1, clip2, clip3, clip4. THE OUTPUT MUST CONTAIN THE FLOW GENERATION SETTINGS BLOCK AND THE FILE NAMING RULE BLOCK.

NO SPLIT SCREEN. NO SIMULTANEOUS OPTIONS. NO MORPHING TRANSITIONS. NO EXTRA TRANSITION SEGMENT. NO EXTRA RUNTIME. NO CUTTING CORNERS.

FOLLOW THE TIMELINE EXACTLY. FOLLOW EVERY GLOBAL RULE EXACTLY. DO NOT OMIT ANY REQUIRED FIELD. DO NOT WEAKEN ANY REQUIREMENT. DO NOT COMPRESS OR IGNORE THE SELF-CHECK.

ONLY OUTPUT THE REQUIRED PRODUCTION-READY STRUCTURE.
"""
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


