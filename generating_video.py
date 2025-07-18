# import numpy as np
# from scipy.io import wavfile
# from moviepy.editor import *
# from proglog import TqdmProgressBarLogger
# from PIL import Image

# # === SETTINGS ===
# AUDIO_FILE = "/files/podcast.wav"
# OUTPUT_FILE = "/files/output_visualizer_fast.mp4"
# #AUDIO_FILE = "podcast.wav"
# #OUTPUT_FILE = "output_visualizer_fast.mp4"
# W, H = 1280, 720
# FPS = 30
# NUM_BARS = 100
# BAR_WIDTH = W // NUM_BARS

# # === LOAD AUDIO ===
# sample_rate, samples = wavfile.read(AUDIO_FILE)
# if samples.ndim == 2:
#     samples = samples.mean(axis=1)
# samples = samples / np.max(np.abs(samples))
# duration = len(samples) / sample_rate
# total_frames = int(duration * FPS)

# # === PRECOMPUTE BAR HEIGHTS PER FRAME ===
# chunk_size = 2048
# frame_amplitudes = []

# for i in range(total_frames):
#     t = i / FPS
#     start = int(t * sample_rate)
#     chunk = samples[start:start + chunk_size]
#     if len(chunk) < chunk_size:
#         chunk = np.pad(chunk, (0, chunk_size - len(chunk)))
#     bar_vals = np.interp(
#         np.linspace(0, len(chunk), NUM_BARS),
#         np.arange(len(chunk)),
#         chunk,
#     )
#     frame_amplitudes.append(bar_vals)

# # === BACKGROUND IMAGE CLIP ===
# bg_image_path = "free-nature-images.jpg"
# resized_image_path = "resized_background.jpg"
# Image.open(bg_image_path).resize((W, H)).save(resized_image_path)

# bg = ImageClip(resized_image_path).set_duration(duration)

# # === FRAME RENDER FUNCTION ===
# def make_waveform_frame(t):
#     frame = np.zeros((H, W, 3), dtype=np.uint8)
#     center_y = H // 2
#     index = int(t * FPS)
#     if index >= len(frame_amplitudes):
#         return frame

#     bars = frame_amplitudes[index]
#     for i, val in enumerate(bars):
#         amp = int(val * 300)
#         x = i * BAR_WIDTH
#         y1 = center_y - abs(amp)
#         y2 = center_y + abs(amp)
#         frame[y1:y2, x:x+3] = [0, 255, 255]

#     return frame

# # === MAKE VIDEO CLIP ===
# waveform_clip = VideoClip(make_waveform_frame, duration=duration)
# final = CompositeVideoClip([bg, waveform_clip]).set_audio(AudioFileClip(AUDIO_FILE))

# # === EXPORT VIDEO WITH PROGRESS BAR ===
# logger = TqdmProgressBarLogger()

# final.write_videofile(
#     OUTPUT_FILE,
#     fps=FPS,
#     codec="libx264",
#     audio_codec="aac",
#     temp_audiofile="temp-audio.m4a",
#     remove_temp=False,
#     logger=logger
# )

















# import numpy as np
# from scipy.io import wavfile
# from scipy.signal import resample
# from PIL import Image, ImageDraw
# import os

# AUDIO_FILE = "/files/podcast.wav"
# OUTPUT_VIDEO = "/files/output_visualizer_fast.mp4"
# FRAMES_DIR = "/files/frames/"
# BG_IMAGE = "free-nature-images.jpg"

# W, H, FPS, NUM_BARS = 1280, 720, 30, 100
# BAR_COLOR = (0, 255, 255)
# BAR_WIDTH = W // NUM_BARS

# os.makedirs(FRAMES_DIR, exist_ok=True)

# # === AUDIO ===
# rate, samples = wavfile.read(AUDIO_FILE)
# if samples.ndim == 2:
#     samples = samples.mean(axis=1)
# samples = samples / np.max(np.abs(samples))
# duration = len(samples) / rate
# total_frames = int(duration * FPS)

# # === BACKGROUND ===
# bg = Image.open(BG_IMAGE).resize((W, H))

# samples_per_frame = int(rate / FPS)

# for frame_idx in range(total_frames):
#     chunk = samples[frame_idx * samples_per_frame : (frame_idx + 1) * samples_per_frame]
#     if len(chunk) < samples_per_frame:
#         chunk = np.pad(chunk, (0, samples_per_frame - len(chunk)))
#     bars = resample(chunk, NUM_BARS)
#     bars = np.abs(bars)

#     frame = bg.copy()
#     draw = ImageDraw.Draw(frame)
#     cy = H // 2
#     for i, amp in enumerate(bars):
#         bar_h = int(amp * (H // 3))
#         x = i * BAR_WIDTH
#         draw.rectangle([x, cy - bar_h, x + BAR_WIDTH - 1, cy + bar_h], fill=BAR_COLOR)

#     frame.save(f"{FRAMES_DIR}/{frame_idx:05d}.png")















































import numpy as np
from scipy.io import wavfile
from scipy.signal import resample
from PIL import Image, ImageDraw
import cv2

AUDIO_FILE = "/files/podcast.wav"
OUTPUT_VIDEO = "/files/output_visualizer_opencv.mp4"

W, H, FPS, NUM_BARS = 1280, 720, 30, 100
BAR_COLOR, BG_COLOR = (0, 255, 255), (0, 0, 0)
BAR_WIDTH = W // NUM_BARS

# === AUDIO ===
rate, samples = wavfile.read(AUDIO_FILE)
if samples.ndim == 2:
    samples = samples.mean(axis=1)
samples = samples / np.max(np.abs(samples))
duration = len(samples) / rate
total_frames = int(duration * FPS)
samples_per_frame = int(rate / FPS)

# === OPENCV VIDEO WRITER ===
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # mp4 codec
video = cv2.VideoWriter(OUTPUT_VIDEO, fourcc, FPS, (W, H))

# === GENERATE FRAMES AND WRITE VIDEO ===
for frame_idx in range(total_frames):
    start = frame_idx * samples_per_frame
    chunk = samples[start : start + samples_per_frame]
    if len(chunk) < samples_per_frame:
        chunk = np.pad(chunk, (0, samples_per_frame - len(chunk)))
    bars = np.abs(resample(chunk, NUM_BARS))

    # Generate frame using PIL
    frame = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(frame)
    cy = H // 2
    for i, amp in enumerate(bars):
        bar_h = int(amp * (H // 3))
        x = i * BAR_WIDTH
        draw.rectangle([x, cy - bar_h, x + BAR_WIDTH - 1, cy + bar_h], fill=BAR_COLOR)

    # Convert PIL frame to OpenCV format
    frame_np = np.array(frame)
    frame_bgr = cv2.cvtColor(frame_np, cv2.COLOR_RGB2BGR)
    video.write(frame_bgr)

video.release()
print("✅ Video created:", OUTPUT_VIDEO)



import subprocess

VIDEO_NO_AUDIO = "/files/output_visualizer_opencv.mp4"
AUDIO_FILE = "/files/podcast.wav"
FINAL_OUTPUT = "/files/output_visualizer.mp4"

# ffmpeg command to merge audio with video
ffmpeg_cmd = [
    "ffmpeg",
    "-y",  # overwrite output file if exists
    "-i", VIDEO_NO_AUDIO,
    "-i", AUDIO_FILE,
    "-c:v", "copy",  # copy video stream without re-encoding
    "-c:a", "aac",   # encode audio in AAC format
    "-shortest",     # cut video to shortest input (sync audio/video)
    FINAL_OUTPUT
]

# Run the ffmpeg command
subprocess.run(ffmpeg_cmd, check=True)

print(f"✅ Final video with audio saved at: {FINAL_OUTPUT}")

